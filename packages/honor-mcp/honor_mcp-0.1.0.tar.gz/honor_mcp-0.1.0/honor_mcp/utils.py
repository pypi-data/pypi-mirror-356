"""Utility functions for Honor MCP."""

from typing import Any, Dict


def format_course_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Format course data from API response into a structured dictionary.

    Args:
        data: The course data response from the API

    Returns:
        A structured dictionary containing course information
    """
    # Check if we have the expected structure in the response
    if "content" not in data or not isinstance(data["content"], list):
        return {"error": "Unexpected API response format"}

    course_list = data["content"]
    total_courses = data.get("totalSize", len(course_list))

    # Format each course with the requested information
    formatted_courses = []
    for course in course_list:
        course_info = {
            "course_name": course.get("courseName", "Unknown"),
            "role": course.get("role", {}).get("name") if course.get("role") else None,
            "topic_count": course.get("topicCount"),
            "assessment_count": course.get("assessmentCount")
        }

        # Add optional fields if they exist
        if course.get("courseIdentifier"):
            course_info["course_identifier"] = course["courseIdentifier"]

        if course.get("startDate"):
            course_info["start_date"] = course["startDate"]

        if course.get("endDate"):
            course_info["end_date"] = course["endDate"]

        formatted_courses.append(course_info)

    # Create the final structured response
    result = {
        "total_courses": total_courses,
        "courses": formatted_courses
    }

    return result
