class TaskNavigationPanel:
    """
    Page Object for Task Navigation Panel.
    Handles stage accordion, task selection, and navigation between tasks.
    """

    def __init__(self, page):
        self.page = page
        # Locators for task navigation panel
        self.navigation_container = page.locator("[class*='task-nav'], [class*='navigation'], aside, [class*='sidebar']")
        self.stage_accordion = page.locator("[class*='stage'], [class*='accordion']")
        self.task_cards = page.locator("[class*='task-card'], [class*='task-item']")

    def click_stage_accordion_by_number(self, stage_number):
        """
        Click/expand a stage accordion by its number.

        Args:
            stage_number: The stage number (1-based index)
        """
        # Try multiple selector strategies
        stage_locators = [
            self.page.locator(f"[class*='stage']:has-text('Stage {stage_number}')"),
            self.page.locator(f"[class*='stage-card']:nth-of-type({stage_number})"),
            self.page.locator(f"[data-stage='{stage_number}']")
        ]

        for locator in stage_locators:
            if locator.count() > 0:
                locator.first.wait_for(state="visible", timeout=10000)
                locator.first.click()
                self.wait_for_tasks_visible()
                return

        # Fallback: click any stage accordion
        if self.stage_accordion.count() > 0:
            self.stage_accordion.nth(stage_number - 1).click()
            self.wait_for_tasks_visible()

    def click_stage_accordion_by_name(self, stage_name):
        """
        Click/expand a stage accordion by its name.

        Args:
            stage_name: The name of the stage
        """
        stage_locator = self.page.locator(f"[class*='stage']:has-text('{stage_name}')")
        stage_locator.first.wait_for(state="visible", timeout=10000)
        stage_locator.first.click()

        self.wait_for_tasks_visible()

    def wait_for_tasks_visible(self, timeout=5000):
        """
        Wait for tasks to become visible after expanding a stage.

        Args:
            timeout: Maximum wait time in milliseconds
        """
        self.page.wait_for_timeout(500)  # Short wait for animation

        # Wait for task cards to be visible
        if self.task_cards.count() > 0:
            self.task_cards.first.wait_for(state="visible", timeout=timeout)

    def click_task_by_number(self, task_number):
        """
        Click a task by its number.

        Args:
            task_number: The task number (1-based index)
        """
        # Try multiple selector strategies
        task_locators = [
            self.page.locator(f"[class*='task']:has-text('Task {task_number}')"),
            self.page.locator(f"[class*='task']:has-text('{task_number}')"),
            self.page.locator(f"[data-task='{task_number}']"),
            self.task_cards.nth(task_number - 1)
        ]

        for locator in task_locators:
            if locator.count() > 0:
                locator.first.scroll_into_view_if_needed()
                locator.first.wait_for(state="visible", timeout=10000)
                locator.first.click()
                self.wait_for_task_content_load()
                return

        raise Exception(f"Task {task_number} not found")

    def click_task_by_name(self, task_name):
        """
        Click a task by its name.

        Args:
            task_name: The name of the task
        """
        task_locator = self.page.locator(f"[class*='task']:has-text('{task_name}')")
        task_locator.first.scroll_into_view_if_needed()
        task_locator.first.wait_for(state="visible", timeout=10000)
        task_locator.first.click()

        self.wait_for_task_content_load()

    def click_first_task(self):
        """
        Click the first available task in the navigation panel.
        """
        # First, ensure a stage is expanded
        if self.task_cards.count() == 0:
            # Try to expand the first stage
            self.click_stage_accordion_by_number(1)

        # Now click the first task
        if self.task_cards.count() > 0:
            self.task_cards.first.scroll_into_view_if_needed()
            self.task_cards.first.wait_for(state="visible", timeout=10000)
            self.task_cards.first.click()
            self.wait_for_task_content_load()
        else:
            raise Exception("No tasks found in navigation panel")

    def wait_for_task_content_load(self, timeout=10000):
        """
        Wait for task content area to load after selecting a task.

        Args:
            timeout: Maximum wait time in milliseconds
        """
        self.page.wait_for_timeout(1000)  # Wait for UI update

        # Wait for parameter panel or task content to be visible
        content_indicators = [
            self.page.locator("[class*='parameter'], [class*='task-content']"),
            self.page.locator("[class*='form'], main")
        ]

        for locator in content_indicators:
            if locator.count() > 0:
                try:
                    locator.first.wait_for(state="visible", timeout=5000)
                    break
                except:
                    continue

    def is_task_marked_complete(self, task_name):
        """
        Check if a task is marked as completed.

        Args:
            task_name: The name of the task

        Returns:
            bool: True if task is completed, False otherwise
        """
        try:
            # Look for completion indicators
            task_locator = self.page.locator(f"[class*='task']:has-text('{task_name}')")

            if task_locator.count() > 0:
                task_element = task_locator.first

                # Check for completion class or checkmark
                has_complete_class = ("complete" in task_element.get_attribute("class") or
                                       "done" in task_element.get_attribute("class"))

                # Check for checkmark icon
                checkmark = task_element.locator("svg[class*='check'], i[class*='check'], [class*='checkmark']")
                has_checkmark = checkmark.count() > 0

                return has_complete_class or has_checkmark

            return False
        except:
            return False

    def get_task_state(self, task_name):
        """
        Get the state of a task.

        Args:
            task_name: The name of the task

        Returns:
            str: Task state (e.g., 'PENDING', 'IN_PROGRESS', 'COMPLETED')
        """
        try:
            task_locator = self.page.locator(f"[class*='task']:has-text('{task_name}')")

            if task_locator.count() > 0:
                task_element = task_locator.first
                classes = task_element.get_attribute("class")

                if "complete" in classes.lower() or "done" in classes.lower():
                    return "COMPLETED"
                elif "progress" in classes.lower() or "active" in classes.lower():
                    return "IN_PROGRESS"
                else:
                    return "PENDING"

            return "UNKNOWN"
        except:
            return "UNKNOWN"

    def scroll_to_task(self, task_name):
        """
        Scroll to a specific task in the navigation panel.

        Args:
            task_name: The name of the task
        """
        task_locator = self.page.locator(f"[class*='task']:has-text('{task_name}')")

        if task_locator.count() > 0:
            task_locator.first.scroll_into_view_if_needed()
            self.page.wait_for_timeout(500)

    def get_all_tasks_count(self):
        """
        Get the total count of visible tasks.

        Returns:
            int: Number of tasks visible in the navigation panel
        """
        return self.task_cards.count()

    def navigate_to_first_stage_first_task(self):
        """
        Navigate to the first task of the first stage.
        """
        self.click_stage_accordion_by_number(1)
        self.click_first_task()
