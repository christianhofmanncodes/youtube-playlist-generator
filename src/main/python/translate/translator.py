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
        german = QLocale(QLocale.Language.German, QLocale.Country.Germany)
        self.trans.load(german, data)
        app.instance().installTranslator(self.trans)

    elif settings_dict["general"][0]["programLanguage"] == "Español":
        data = app_context.get_resource(f"forms/translations/es-ES/{qm_file}")
        german = QLocale(QLocale.Language.Spanish, QLocale.Country.Spain)
        self.trans.load(german, data)
        app.instance().installTranslator(self.trans)
