def generate_explanation(stem: str, options: list, correct_label: str, source_ref: str|None=None):
    # شرح تعليمي مختصر + لماذا الخيارات الأخرى خاطئة (Stub)
    bullets = []
    bullets.append(f"الإجابة الصحيحة هي ({correct_label}) بناءً على المنطق السريري الشائع.")
    for opt in options:
        lab = opt.get("label")
        txt = opt.get("text","")
        if lab == correct_label:
            bullets.append(f"({lab}) يطابق القراءة/التوصيات المرجّحة للسؤال.")
        else:
            bullets.append(f"({lab}) غير مرجّحة هنا بسبب عدم توافقها مع المعطيات السريرية.")
    ref = source_ref or "مرجع تعليمي عام"
    md = "\n".join([f"- {b}" for b in bullets]) + f"\n\n> مرجع: {ref}\n\n**تنبيه**: هذا المحتوى للتعليم فقط وليس بديلاً عن الاستشارة الطبية."
    return md
