def safety_filter(md: str) -> str:
    # إزالة/تحييد عبارات قد تُفسَّر كخطة علاج مباشرة
    blocked = ["جرعة", "mg", "ملغ", "وصفة", "استبدال الدواء"]
    for w in blocked:
        md = md.replace(w, "[تم الحجب تعليميًا]")
    return md
