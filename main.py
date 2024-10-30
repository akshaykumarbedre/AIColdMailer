import logging
import streamlit as st
from src.config import Config
from src.services.automation import ColdEmailAutomation
from src.ui.streamlit_app import StreamlitUI

logger = logging.getLogger(__name__)

def main():
    try:
        config = Config.load_from_env()
        automation = ColdEmailAutomation(config)
        ui = StreamlitUI(automation)
        ui.run()
    except Exception as e:
        logger.critical(f"Application failed to start: {str(e)}")
        st.error("An unexpected error occurred. Please check the logs for details.")

if __name__ == "__main__":
    main()