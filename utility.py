import re
import logging
import time
import traceback
from collections import defaultdict
import os

# Set up advanced logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Timer utility to track performance
class Timer:
    def __init__(self):
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def end(self):
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            return elapsed_time
        return None

    def log_time(self, context=""):
        elapsed_time = self.end()
        logger.info(f"{context} took {elapsed_time:.4f} seconds")

# State-of-the-art utility to convert Struts to Spring MVC JSP with logging and error handling
def convert_struts_to_spring(struts_jsp):
    # Initialize timer for performance logging
    timer = Timer()
    timer.start()

    logger.info("Starting Struts 1.x to Spring MVC JSP conversion...")

    tag_replacement_map = {
        # **HTML Tag Library** (Struts HTML tags to Spring equivalents)
        r'<html:html>': '<html>',
        r'</html:html>': '</html>',
        r'<html:base>': '<base href="${pageContext.request.contextPath}">',
        r'<html:form': '<form:form',
        r'</html:form>': '</form:form>',
        r'<html:text': '<form:input',
        r'<html:password': '<form:password',
        r'<html:textarea': '<form:textarea',
        r'<html:checkbox': '<form:checkbox',
        r'<html:radio': '<form:radiobutton>',
        r'<html:select': '<form:select>',
        r'</html:select>': '</form:select>',
        r'<html:options': '<form:options>',
        r'</html:options>': '</form:options>',
        r'<html:option': '<form:option>',
        r'</html:option>': '</form:option>',
        r'<html:hidden>': '<form:hidden>',
        r'<html:reset>': '<input type="reset">',
        r'<html:submit>': '<form:button type="submit">',
        r'<html:button>': '<form:button>',
        r'<html:file>': '<form:input type="file">',
        r'<html:link>': '<a href="<c:url value="${link}" />">',
        r'<html:img>': '<img src="<c:url value="${imageUrl}" />">',
    }

    # **Logic Tag Library** (Struts conditional logic and iteration tags)
    logic_tags_map = {
        r'<logic:equal\s+value="([^"]+)"\s*name="([^"]+)"\s*/>': r'<c:if test="${{ {name} == \1 }}">',
        r'<logic:notEqual\s+value="([^"]+)"\s*name="([^"]+)"\s*/>': r'<c:if test="${{ {name} != \1 }}">',
        r'<logic:greaterThan\s+value="([^"]+)"\s*name="([^"]+)"\s*/>': r'<c:if test="${{ {name} > \1 }}">',
        r'<logic:lessThan\s+value="([^"]+)"\s*name="([^"]+)"\s*/>': r'<c:if test="${{ {name} < \1 }}">',
        r'<logic:empty\s*name="([^"]+)"\s*/>': r'<c:if test="${empty {name}}">',
        r'<logic:notEmpty\s*name="([^"]+)"\s*/>': r'<c:if test="${not empty {name}}">',
        r'<logic:iterate\s+id="([^"]+)"\s+name="([^"]+)"\s*(.*?)</logic:iterate>': r'<c:forEach var="\1" items="${\2}">\3</c:forEach>',
        r'<logic:forward\s+name="([^"]+)"\s+path="([^"]+)"\s*/>': r'<c:redirect url="\2"/>',
    }

    # **Bean Tag Library** (Handle Struts Bean tags and messages)
    bean_tags_map = {
        r'<bean:message\s+key="([^"]+)"\s*/>': r'<spring:message code="\1"/>',
        r'<bean:write\s+name="([^"]+)"\s*/>': r'<c:out value="${\1}"/>',
        r'<bean:define\s+name="([^"]+)"\s+property="([^"]+)"\s*/>': r'<c:set var="\1" value="${\1.\2}"/>',
        r'<bean:resource\s+name="([^"]+)"\s*/>': r'<c:url value="\1"/>',
    }

    # **Tiles Tag Library** (Tiles tags for templating in Struts)
    tiles_tags_map = {
        r'<tiles:insert\s+page="([^"]+)"\s*/>': r'<jsp:include page="\1"/>',  # Simple Tiles insert
        r'<tiles:put\s+name="([^"]+)"\s*value="([^"]+)"\s*/>': r'<c:set var="\1" value="\2"/>',  # Inserting data into Tiles
        r'<tiles:putList\s+name="([^"]+)"\s*value="([^"]+)"\s*/>': r'<c:set var="\1" value="\2"/>',
    }

    # **Nested Tag Library** (Handle nested properties and data)
    nested_tags_map = {
        r'<nested:write\s+name="([^"]+)"\s*/>': r'<c:out value="${\1}"/>',
        r'<nested:form\s+name="([^"]+)"\s*method="([^"]+)"\s*/>': r'<form:form modelAttribute="\1" method="\2">',
    }

    # **Conversion Process:**
    def process_conversion(tags_map, tag_type):
        logger.info(f"Processing {tag_type} tags...")
        for struts_tag, spring_tag in tags_map.items():
            try:
                logger.debug(f"Replacing Struts tag: {struts_tag} with Spring tag: {spring_tag}")
                struts_jsp = re.sub(struts_tag, spring_tag, struts_jsp)
            except Exception as e:
                logger.error(f"Error replacing tag: {struts_tag} to {spring_tag}. Exception: {str(e)}")
                logger.debug(traceback.format_exc())  # Logs the complete error stack trace
        return struts_jsp

    # Apply all tag replacements
    struts_jsp = process_conversion(tag_replacement_map, "HTML")
    struts_jsp = process_conversion(logic_tags_map, "Logic")
    struts_jsp = process_conversion(bean_tags_map, "Bean")
    struts_jsp = process_conversion(tiles_tags_map, "Tiles")
    struts_jsp = process_conversion(nested_tags_map, "Nested")

    # Log the conversion time
    timer.log_time("JSP conversion")

    logger.info("Conversion complete.")
    return struts_jsp


# Function to read, process, and write files
def process_file(input_file_path, output_file_path=None):
    # Ensure the file exists
    if not os.path.isfile(input_file_path):
        logger.error(f"File {input_file_path} does not exist.")
        return

    # Read the input JSP file
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        struts_jsp = input_file.read()

    # Convert the JSP content
    converted_jsp = convert_struts_to_spring(struts_jsp)

    # Optionally save the converted JSP to a file
    if output_file_path:
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(converted_jsp)
        logger.info(f"Converted JSP saved to {output_file_path}")
    else:
        logger.info("Converted JSP (no output file specified):")
        logger.info(converted_jsp)


if __name__ == "__main__":
    # Example usage:
    input_file_path = 'path/to/your/input.jsp'  # Replace with actual input file path
    output_file_path = 'path/to/your/output.jsp'  # Optionally replace with output path

    # Process the JSP file
    process_file(input_file_path, output_file_path)
