#!/usr/bin/env python3
import hashlib
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, ClassVar, Dict, List, Optional, Type

import envo.e2e
from envo import const, logger, logs, shell, utils
from envo.env import Env, ShellEnv
from envo.environ import environ
from envo.exceptions import UserError, user_code
from envo.shell import FancyShell, PromptBase, PromptState, Shell
from envo.status import Status
from envo.utils import Callback, import_env_from_file

package_root = Path(os.path.realpath(__file__)).parent

if envo.e2e.enabled:
    templates_dir = package_root.parent / "tests/templates"
else:
    templates_dir = package_root / "templates"


__all__ = ["_main"]


class CantFindEnvFile(UserError):
    def __init__(self):
        super().__init__(const.msgs.could_not_find_env)


class NormalPrompt(PromptBase):
    msg: str = ""

    @property
    def p_name(self) -> str:
        return f"({self.name})" if self.name else ""

    @property
    def p_msg(self) -> str:
        return f"{{BOLD_RED}}{self.msg}{{RESET}}\n" if self.msg else ""

    def __init__(self) -> None:
        super().__init__()

        self.state_prefix_map = {
            PromptState.LOADING: lambda: f"{self.p_msg}{const.emojis['loading']}{self.p_name}{self.default}",
            PromptState.NORMAL: lambda: f"{self.p_msg}{self.emoji}{self.p_name}{self.default}",
        }


class HeadlessMode:
    @dataclass
    class Links:
        shell: Shell

    @dataclass
    class Sets:
        stage: str
        msg: str
        env_path: Path

    shell_env: ShellEnv
    blocking: bool = True
    prompt: NormalPrompt

    def __init__(self, se: Sets, li: Links) -> None:
        self.se = se
        self.li = li

        self.extra_watchers = []

        self.status = Status(
            calls=Status.Callbacks(
                on_ready=Callback(self._on_ready),
                on_not_ready=Callback(self._on_not_ready),
            )
        )

        self.shell_env = None

        self.li.shell.set_full_traceback_enabled(True)

        logger.set_level(logs.Level.INFO)

        logger.debug("Creating Headless Mode")

    def _on_ready(self) -> None:
        self.prompt.state = PromptState.NORMAL
        self.li.shell.set_prompt(self.prompt.as_str())

    def _on_not_ready(self) -> None:
        self.prompt.state = PromptState.LOADING
        self.li.shell.set_prompt(self.prompt.as_str())

    def unload(self) -> None:
        if self.shell_env:
            self.shell_env._unload()

        self.li.shell.calls.reset()

    def init(self) -> None:
        self.li.shell.set_context({"logger": logger})

        self._create_env()

        self.prompt = NormalPrompt()
        self.prompt.state = PromptState.LOADING
        self.prompt.msg = self.se.msg
        self.prompt.emoji = self.shell_env.env.meta.emoji
        self.prompt.name = self.shell_env.get_name()

        self.li.shell.set_prompt(str(self.prompt))

        self.li.shell.set_variable("env", self.shell_env.env)
        self.li.shell.set_variable("environ", os.environ)

        self.shell_env.activate()
        self.shell_env.load()

    def get_env_file(self) -> Path:
        return self.se.env_path

    def _create_env_object(self, file: Path) -> ShellEnv:
        with user_code():
            env = import_env_from_file(file).ThisEnv()

        shell_env = ShellEnv(
            li=ShellEnv._Links(shell=self.li.shell, status=self.status, env=env),
            se=ShellEnv._Sets(
                blocking=self.blocking,
            ),
        )
        return shell_env

    def _create_env(self) -> None:
        env_file = self.get_env_file()
        logger.debug(f'Creating Env from file "{env_file}"')

        # unload modules
        for m in list(sys.modules.keys())[:]:
            if m.startswith("env_"):
                sys.modules.pop(m)
        try:
            self.shell_env = self._create_env_object(env_file)
        except ImportError as exc:
            logger.traceback()
            raise UserError(f"""Couldn't import "{env_file}" ({exc}).""")


class NormalMode(HeadlessMode):
    @dataclass
    class Links(HeadlessMode.Links):
        pass

    @dataclass
    class Sets(HeadlessMode.Sets):
        pass

    shell_env: ShellEnv
    blocking: bool = False

    def __init__(self, se: Sets, li: Links) -> None:
        super(NormalMode, self).__init__(se=se, li=li)
        self.se = se
        self.li = li

        self.li.shell.set_full_traceback_enabled(True)

        logger.debug("Creating NormalMode")

    def stop(self) -> None:
        self.shell_env._exit()


class EnvoBase:
    @dataclass
    class Sets:
        stage: Optional[str]

    shell: shell.Shell
    mode: Optional[HeadlessMode]
    env_dirs: List[Path]

    def __init__(self, se: Sets):
        self.se = se
        logger.set_level(logs.Level.INFO)
        self.mode = None

        self.env_dirs = self._get_env_dirs()

    def _get_env_dirs(self) -> List[Path]:
        ret = []
        path = Path(".").absolute()
        while True:
            if path.parent == path:
                break

            for p in path.glob("env_*.py"):
                if p.parent not in ret:
                    ret.append(p.parent)

            path = path.parent

        return ret

    def find_env(self) -> Path:
        # TODO: Test this
        if not self.env_dirs:
            raise CantFindEnvFile()

        directory = self.env_dirs[0]

        if self.se.stage:
            ret = directory / f"env_{self.se.stage}.py"
            if not ret.exists():
                raise CantFindEnvFile()
            return ret
        else:
            ret_stage = None
            ret = None
            for p in directory.glob("env_*.py"):
                stage = const.STAGES.filename_to_stage(p.name)
                if not ret_stage or stage.priority >= ret_stage.priority:
                    ret_stage = stage
                    ret = p

            return ret

    @property
    def data_dir_name(self) -> str:
        hash_object = hashlib.md5(str(self.find_env()).encode("utf-8"))
        ret = hash_object.hexdigest()
        return ret

    def init(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError()

    def single_command(self, command: str) -> None:
        raise NotImplementedError()

    def dry_run(self) -> None:
        raise NotImplementedError()

    def dump(self) -> None:
        raise NotImplementedError()


class EnvoHeadless(EnvoBase):
    @dataclass
    class Sets(EnvoBase.Sets):
        stage: Optional[str]

    shell: shell.Shell
    mode: HeadlessMode

    def __init__(self, se: Sets):
        super().__init__(se)
        self.se = se
        logger.set_level(logs.Level.INFO)

        if not self.env_dirs:
            raise CantFindEnvFile

    def on_error(self, exc: Exception) -> None:
        logger.error(exc)

    def init(self, *args: Any, **kwargs: Any) -> None:
        self.mode = HeadlessMode(
            se=HeadlessMode.Sets(
                stage=self.se.stage,
                msg="",
                env_path=self.find_env(),
            ),
            li=HeadlessMode.Links(shell=self.shell),
        )
        self.mode.init()

    def single_command(self, command: str) -> None:
        self.shell = Shell.create(Shell.Callbacks(), data_dir_name=self.data_dir_name)
        self.init()

        try:
            self.shell.default(command)
        except SystemExit as e:
            sys.exit(e.code)
        else:
            sys.exit(self.shell.last_return_code)

    def dry_run(self) -> None:
        self.shell = Shell.create(Shell.Callbacks(), data_dir_name=self.data_dir_name)
        self.init()
        content = "\n".join([f'export {k}="{v}"' for k, v in self.mode.shell_env.env.get_env_vars().items()])
        print(content)

    def dump(self) -> None:
        self.shell = Shell.create(Shell.Callbacks(), data_dir_name=self.data_dir_name)
        self.init()
        path = self.mode.shell_env.env.dump_dot_env()
        logger.info(f"Saved envs to {str(path)} 💾")


class Envo(EnvoBase):
    @dataclass
    class Sets(EnvoBase.Sets):
        pass

    environ_before = Dict[str, str]
    quit: bool
    mode: HeadlessMode

    def __init__(self, se: Sets) -> None:
        super().__init__(se)

        self.quit: bool = False
        self.environ_before = os.environ.copy()  # type: ignore

    def init(self, *args: Any, **kwargs: Any) -> None:
        if self.mode:
            self.mode.unload()

        self.mode = NormalMode(
            se=NormalMode.Sets(
                stage=self.se.stage,
                msg="",
                env_path=self.find_env(),
            ),
            li=NormalMode.Links(shell=self.shell),
        )
        self.mode.init()

    def spawn_shell(self) -> None:
        """
        :param type: shell type
        """

        def on_ready():
            pass

        self.shell = FancyShell.create(
            calls=FancyShell.Callbacks(on_ready=Callback(on_ready)),
            data_dir_name=self.data_dir_name,
        )
        self.init()

        self.mode.shell_env.on_shell_create()

        self.shell.start()
        self.mode.unload()


class EnvoCreator:
    @dataclass
    class Sets:
        stage: str

    def __init__(self, se: Sets) -> None:
        logger.debug("Starting EnvoCreator")
        self.se = se

    def _create_from_templ(self, stage: str) -> None:
        """
        Create env file from template.

        :param templ_file:
        :param output_file:
        :param is_comm:
        :return:
        """
        output_file = Path(f"env_{stage}.py")

        parent = "env_comm" if stage != "comm" else None

        if output_file.exists():
            raise UserError(f"{str(output_file)} file already exists.")

        env_dir = Path(".").absolute()
        package_name = utils.dir_name_to_pkg_name(env_dir.name)
        class_name = f"{utils.dir_name_to_class_name(package_name)}{stage.capitalize()}Env"

        context = {
            "class_name": class_name,
            "name": env_dir.name,
            "stage": stage,
            "emoji": const.STAGES.get_stage_name_to_emoji().get(stage, "🙂"),
            "base_class": "ParentEnv" if parent else Env.__name__,
            "this_env": const.THIS_ENV,
        }

        if stage == "comm":
            templ_file = Path("comm_env.py.templ")
        else:
            context["parent_module"] = parent
            templ_file = Path("env.py.templ")

        utils.render_py_file(templates_dir / templ_file, output=output_file, context=context)

    def create(self) -> None:
        if not self.se.stage:
            self.se.stage = "comm"

        self._create_from_templ(self.se.stage)

        if self.se.stage != "comm" and not Path("env_comm.py").exists():
            self._create_from_templ("comm")

        print(f"Created {self.se.stage} environment 🍰!")


@dataclass
class BaseOption:
    stage: str
    body: str

    keywords: ClassVar[str] = NotImplemented

    def run(self) -> None:
        raise NotImplementedError()


@dataclass
class Command(BaseOption):
    def run(self) -> None:
        envo.e2e.envo = env_headless = EnvoHeadless(EnvoHeadless.Sets(stage=self.stage))
        env_headless.single_command(self.body)


@dataclass
class DryRun(BaseOption):
    def run(self) -> None:
        envo.e2e.envo = env_headless = EnvoHeadless(EnvoHeadless.Sets(stage=self.stage))
        env_headless.dry_run()


@dataclass
class Dump(BaseOption):
    def run(self) -> None:
        envo.e2e.envo = env_headless = EnvoHeadless(EnvoHeadless.Sets(stage=self.stage))
        env_headless.dump()


@dataclass
class Version(BaseOption):
    def run(self) -> None:
        from envo.__version__ import __version__

        print(__version__)


@dataclass
class Init(BaseOption):
    def run(self) -> None:
        stage = self.stage or "comm"
        envo_creator = EnvoCreator(EnvoCreator.Sets(stage=stage))
        envo_creator.create()


@dataclass
class Start(BaseOption):
    def run(self) -> None:
        envo.e2e.envo = e = Envo(Envo.Sets(stage=self.stage))
        e.spawn_shell()


option_name_to_option: Dict[str, Type[BaseOption]] = {
    "-c": Command,
    "run": Command,
    "dry-run": DryRun,
    "dump": Dump,
    "": Start,
    "init": Init,
    "version": Version,
}


def _main() -> None:
    logger.debug("Starting")

    argv = sys.argv[1:]
    keywords = ["init", "dry-run", "version", "dump", "run"]

    stage = environ.stage

    if argv and argv[0] not in keywords:
        stage = argv[0]
        option_name = argv[1] if len(argv) >= 2 else ""
        body = " ".join(argv[2:])
    else:
        option_name = argv[0] if len(argv) >= 1 else ""
        body = " ".join(argv[1:])

    option = option_name_to_option[option_name](stage, body=body)

    try:
        option.run()
    except UserError as e:
        logger.error(str(e))
        if envo.e2e.enabled:
            envo.e2e.on_exit()
        sys.exit(1)
    finally:
        if envo.e2e.enabled:
            envo.e2e.on_exit()


if __name__ == "__main__":
    _main()
