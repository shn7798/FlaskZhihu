# -*- coding: utf-8 -*-
from FlaskZhihu.application import create_app
from FlaskZhihu.settings import TestSettings
if __name__ == '__main__':
    app = create_app(settings=TestSettings())
    app.run()
