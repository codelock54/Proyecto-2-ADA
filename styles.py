from PyQt6.QtWidgets import *

class Styles:
    """Add Styles to User Interface"""
    @staticmethod
    def apply_styles(main_window):
        main_window.widget.setStyleSheet("background-color: #f0f0f0;")

        button_style = """
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
            }
            QPushButton:hover {background-color: #45a049;}
            QPushButton:pressed {background-color: #45a049;}
        """
        main_window.photo_button.setStyleSheet(button_style)
        main_window.record_button.setStyleSheet(button_style)

        close_button_style = """
            QPushButton#closeButton {
                background-color: #f44336;
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
            }
            QPushButton#closeButton:hover {background-color: #d32f2f;}
            QPushButton#closeButton:pressed {background-color: #d32f2f;}
        """
        main_window.findChild(QPushButton, "closeButton").setStyleSheet(close_button_style)


 # def apply_styles(self):
    #     self.widget.setStyleSheet("background-color: #f0f0f0;")

    #     button_style = """
    #         QPushButton {
    #             background-color: #4CAF50;
    #             border: none;
    #             color: white;
    #             padding: 10px 20px;
    #             text-align: center;
    #             text-decoration: none;
    #             display: inline-block;
    #             font-size: 16px;
    #             margin: 4px 2px;
    #             cursor: pointer;
    #             border-radius: 8px;
    #         }
    #         QPushButton:hover {background-color: #45a049;}
    #         QPushButton:pressed {background-color: #45a049;}
    #     """
    #     self.photo_button.setStyleSheet(button_style)
    #     self.record_button.setStyleSheet(button_style)

    #     close_button_style = """
    #         QPushButton#closeButton {
    #             background-color: #f44336;
    #             border: none;
    #             color: white;
    #             padding: 10px 20px;
    #             text-align: center;
    #             text-decoration: none;
    #             display: inline-block;
    #             font-size: 16px;
    #             margin: 4px 2px;
    #             cursor: pointer;
    #             border-radius: 8px;
    #         }
    #         QPushButton#closeButton:hover {background-color: #d32f2f;}
    #         QPushButton#closeButton:pressed {background-color: #d32f2f;}
    #     """
    #     self.findChild(QPushButton, "closeButton").setStyleSheet(close_button_style)
