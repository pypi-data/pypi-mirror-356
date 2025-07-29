from .annotation.__main__ import *
from .data.__main__ import *
from .export.__main__ import *
from .extension.__main__ import *
from .layout.__main__ import *
from .legend.__main__ import *
from .plot.__main__ import *
from .recording.__main__ import *
from .session.__main__ import *
from .tecutil.__main__ import *
from .text.__main__ import *

from .test_exception import *
from .test_macro import *
from .test_version import *


if __name__ == '__main__':
    import test
    test.main()
