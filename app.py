# -*- coding: utf-8 -*-
from FlaskZhihu.application import create_app
from FlaskZhihu.settings import TestSettings, RedisCacheSettings
if __name__ == '__main__':
    #settings = TestSettings()
    settings = RedisCacheSettings()
    app = create_app(settings=settings)
    app.run()
