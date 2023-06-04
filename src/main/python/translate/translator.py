"""module translate.translator"""

import logging

from PyQt5.QtCore import QLocale, QTranslator


def install_translator(
    self, app, app_context, settings_dict: dict, qm_file: str
) -> None:
    """Installs the Translator based on the program language settings."""
    self.trans = QTranslator(self)

    if settings_dict["general"][0]["programLanguage"] == "English":
        logging.info("Program language is English.")

    elif settings_dict["general"][0]["programLanguage"] == "Deutsch":
        data = app_context.get_resource(f"forms/translations/de/{qm_file}")
        german = QLocale(
            language=QLocale.Language.German, country=QLocale.Country.Germany
        )
        self.trans.load(german, data)
        app.instance().installTranslator(self.trans)

    elif settings_dict["general"][0]["programLanguage"] == "Español":
        data = app_context.get_resource(f"forms/translations/es-ES/{qm_file}")
        spanish = QLocale(
            language=QLocale.Language.Spanish, country=QLocale.Country.Spain
        )
        self.trans.load(spanish, data)
        app.instance().installTranslator(self.trans)

    elif settings_dict["general"][0]["programLanguage"] == "Polski":
        data = app_context.get_resource(f"forms/translations/pl/{qm_file}")
        polish = QLocale(
            language=QLocale.Language.Polish, country=QLocale.Country.Poland
        )
        self.trans.load(polish, data)
        app.instance().installTranslator(self.trans)
