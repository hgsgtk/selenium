# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import UnexpectedTagNameException
from selenium.webdriver.common.by import By


class Select:

    def __init__(self, webelement) -> None:
        """
        Constructor. A check is made that the given element is, indeed, a SELECT tag. If it is not,
        then an UnexpectedTagNameException is thrown.

        :Args:
         - webelement - SELECT element to wrap

        Example:
            from selenium.webdriver.support.ui import Select \n
            Select(driver.find_element(By.TAG_NAME, "select")).select_by_index(2)
        """
        if webelement.tag_name.lower() != "select":
            raise UnexpectedTagNameException(
                "Select only works on <select> elements, not on <%s>" %
                webelement.tag_name)
        if not webelement.is_enabled():
            raise NotImplementedError("Select element is disabled and may not be used.")
        self._el = webelement
        multi = self._el.get_dom_attribute("multiple")
        self.is_multiple = multi and multi != "false"

    @property
    def options(self):
        """Returns a list of all options belonging to this select tag"""
        return self._el.find_elements(By.TAG_NAME, 'option')

    @property
    def all_selected_options(self):
        """Returns a list of all selected options belonging to this select tag"""
        return [opt for opt in self.options if opt.is_selected()]

    @property
    def first_selected_option(self):
        """The first selected option in this select tag (or the currently selected option in a
        normal select)"""
        for opt in self.options:
            if opt.is_selected():
                return opt
        raise NoSuchElementException("No options are selected")

    def select_by_value(self, value):
        """Select all options that have a value matching the argument. That is, when given "foo" this
           would select an option like:

           <option value="foo">Bar</option>

           :Args:
            - value - The value to match against

           throws NoSuchElementException If there is no option with specified value in SELECT
           """
        css = "option[value =%s]" % self._escape_string(value)
        opts = self._el.find_elements(By.CSS_SELECTOR, css)
        matched = False
        for opt in opts:
            self._set_selected(opt)
            if not self.is_multiple:
                return
            matched = True
        if not matched:
            raise NoSuchElementException("Cannot locate option with value: %s" % value)

    def select_by_index(self, index):
        """Select the option at the given index. This is done by examining the "index" attribute of an
           element, and not merely by counting.

           :Args:
            - index - The option at this index will be selected

           throws NoSuchElementException If there is no option with specified index in SELECT
           """
        match = str(index)
        for opt in self.options:
            if opt.get_attribute("index") == match:
                self._set_selected(opt)
                return
        raise NoSuchElementException("Could not locate element with index %d" % index)

    def select_by_visible_text(self, text):
        """Select all options that display text matching the argument. That is, when given "Bar" this
           would select an option like:

            <option value="foo">Bar</option>

           :Args:
            - text - The visible text to match against

            throws NoSuchElementException If there is no option with specified text in SELECT
           """
        xpath = ".//option[normalize-space(.) = %s]" % self._escape_string(text)
        opts = self._el.find_elements(By.XPATH, xpath)
        matched = False
        for opt in opts:
            self._set_selected(opt)
            if not self.is_multiple:
                return
            matched = True

        if len(opts) == 0 and " " in text:
            sub_string_without_space = self._get_longest_token(text)
            if sub_string_without_space == "":
                candidates = self.options
            else:
                xpath = ".//option[contains(.,%s)]" % self._escape_string(sub_string_without_space)
                candidates = self._el.find_elements(By.XPATH, xpath)
            for candidate in candidates:
                if text == candidate.text:
                    self._set_selected(candidate)
                    if not self.is_multiple:
                        return
                    matched = True

        if not matched:
            raise NoSuchElementException("Could not locate element with visible text: %s" % text)

    def deselect_all(self) -> None:
        """Clear all selected entries. This is only valid when the SELECT supports multiple selections.
           throws NotImplementedError If the SELECT does not support multiple selections
        """
        if not self.is_multiple:
            raise NotImplementedError("You may only deselect all options of a multi-select")
        for opt in self.options:
            self._unset_selected(opt)

    def deselect_by_value(self, value):
        """Deselect all options that have a value matching the argument. That is, when given "foo" this
           would deselect an option like:

            <option value="foo">Bar</option>

           :Args:
            - value - The value to match against

            throws NoSuchElementException If there is no option with specified value in SELECT
        """
        if not self.is_multiple:
            raise NotImplementedError("You may only deselect options of a multi-select")
        matched = False
        css = "option[value = %s]" % self._escape_string(value)
        opts = self._el.find_elements(By.CSS_SELECTOR, css)
        for opt in opts:
            self._unset_selected(opt)
            matched = True
        if not matched:
            raise NoSuchElementException("Could not locate element with value: %s" % value)

    def deselect_by_index(self, index):
        """Deselect the option at the given index. This is done by examining the "index" attribute of an
           element, and not merely by counting.

           :Args:
            - index - The option at this index will be deselected

            throws NoSuchElementException If there is no option with specified index in SELECT
        """
        if not self.is_multiple:
            raise NotImplementedError("You may only deselect options of a multi-select")
        for opt in self.options:
            if opt.get_attribute("index") == str(index):
                self._unset_selected(opt)
                return
        raise NoSuchElementException("Could not locate element with index %d" % index)

    def deselect_by_visible_text(self, text):
        """Deselect all options that display text matching the argument. That is, when given "Bar" this
           would deselect an option like:

           <option value="foo">Bar</option>

           :Args:
            - text - The visible text to match against
        """
        if not self.is_multiple:
            raise NotImplementedError("You may only deselect options of a multi-select")
        matched = False
        xpath = ".//option[normalize-space(.) = %s]" % self._escape_string(text)
        opts = self._el.find_elements(By.XPATH, xpath)
        for opt in opts:
            self._unset_selected(opt)
            matched = True
        if not matched:
            raise NoSuchElementException("Could not locate element with visible text: %s" % text)

    def _set_selected(self, option) -> None:
        if not option.is_selected():
            if not option.is_enabled():
                raise NotImplementedError("You may not select a disabled option")
            option.click()

    def _unset_selected(self, option) -> None:
        if option.is_selected():
            option.click()

    def _escape_string(self, value: str) -> str:
        if '"' in value and "'" in value:
            substrings = value.split("\"")
            result = ["concat("]
            for substring in substrings:
                result.append("\"%s\"" % substring)
                result.append(", '\"', ")
            result = result[0:-1]
            if value.endswith('"'):
                result.append(", '\"'")
            return "".join(result) + ")"

        if '"' in value:
            return "'%s'" % value

        return "\"%s\"" % value

    def _get_longest_token(self, value: str) -> str:
        items = value.split(" ")
        longest = ""
        for item in items:
            if len(item) > len(longest):
                longest = item
        return longest
