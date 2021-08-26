import re


def get_info_salary(text_salary):
    min_template = r"от\s+(\d+\s\d+)\s(.+)$"
    max_template = r"до\s+(\d+\s\d+)\s(.+)$"
    all_template = r"(\d+\s\d+)\s+[—,–]\s+(\d+\s\d+)\s(.+)$"

    result = re.search(min_template, text_salary)
# 'от   80 000 руб.'
    if result:
        min_salary_text = result.group(1)
        min_salary_text = re.sub(r"\s", "", min_salary_text)

        currency = result.group(2).replace(".", "").replace("/месяц", "")

        return {"min": int(min_salary_text), "max": "", "currency": currency}

    result = re.search(max_template, text_salary)

    if result:
        max_salary_text = result.group(1)
        max_salary_text = re.sub(r"\s", "", max_salary_text)

        currency = result.group(2).replace(".", "").replace("/месяц", "")

        return {"min": "", "max": int(max_salary_text), "currency": currency}

    result = re.search(all_template, text_salary)

    if result:
        min_salary_text = result.group(1)
        min_salary_text = re.sub(r"\s", "", min_salary_text)

        max_salary_text = result.group(2)
        max_salary_text = re.sub(r"\s", "", max_salary_text)

        currency = result.group(3).replace(".", "").replace("/месяц", "")

        return {"min": int(min_salary_text), "max": int(max_salary_text), "currency": currency}

    return {"min": "", "max": "", "currency": ""}
