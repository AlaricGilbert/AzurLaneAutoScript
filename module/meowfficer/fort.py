from module.base.timer import Timer
from module.combat.assets import GET_ITEMS_1
from module.logger import logger
from module.meowfficer.assets import *
from module.meowfficer.base import MeowfficerBase
from module.ui.assets import MEOWFFICER_GOTO_DORM


class MeowfficerFort(MeowfficerBase):
    def meow_chores(self, skip_first_screenshot=True):
        """
        Loop through all chore mechanics to
        get fort xp points

        Args:
            skip_first_screenshot (bool): Skip first
            screen shot or not

        Pages:
            in: MEOWFFICER_FORT
            out: MEOWFFICER_FORT
        """
        self.interval_clear(GET_ITEMS_1)
        check_timer = Timer(1, count=2)
        confirm_timer = Timer(1.5, count=4).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.device.screenshot()

            if self.appear(MEOWFFICER_FORT_GET_XP_1) or \
                    self.appear(MEOWFFICER_FORT_GET_XP_2):
                check_timer.reset()
                confirm_timer.reset()
                continue

            if self.appear(GET_ITEMS_1, offset=5, interval=3):
                self.device.click(MEOWFFICER_FORT_CHECK)
                check_timer.reset()
                confirm_timer.reset()
                continue

            if check_timer.reached():
                is_chore = self.image_color_count(
                    MEOWFFICER_FORT_CHORE, color=(247, 186, 90),
                    threshold=235, count=50)
                check_timer.reset()
                if is_chore:
                    self.device.click(MEOWFFICER_FORT_CHORE)
                    confirm_timer.reset()
                    continue

            # End
            if self.appear(MEOWFFICER_FORT_CHECK, offset=(20, 20)):
                if confirm_timer.reached():
                    break
            else:
                confirm_timer.reset()

    def meow_fort(self):
        """
        Performs fort chores if available,
        applies to every meowfficer simultaneously

        Pages:
            in: page_meowfficer
            out: page_meowfficer
        """
        # Check for fort red notification
        if not self.appear(MEOWFFICER_FORT_RED_DOT):
            return False
        logger.hr('Meowfficer fort', level=1)

        # Enter MEOWFFICER_FORT window
        self.ui_click(MEOWFFICER_FORT_ENTER, check_button=MEOWFFICER_FORT_CHECK, additional=self.meow_additional,
                      retry_wait=3, confirm_wait=0, skip_first_screenshot=True)

        # Perform fort chore operations
        self.meow_chores()

        # Exit back into page_meowfficer
        def additional():
            if self.appear_then_click(GET_ITEMS_1, offset=5, interval=3):
                return True
            return False

        self.ui_click(MEOWFFICER_GOTO_DORM,
                      check_button=MEOWFFICER_FORT_ENTER, appear_button=MEOWFFICER_FORT_CHECK,
                      additional=additional, offset=None, confirm_wait=0, skip_first_screenshot=True)

        return True
