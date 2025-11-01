# med-mcq-backend (MVP)

Backend جاهز لتطبيق بنك أسئلة MCQ لطلبة الطب — FastAPI + SQLite + CSV Import + شرح AI (Stub).

## التشغيل السريع
```bash
cp .env.example .env
# لو عندك Docker
docker compose up --build
# أو محليًا:
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
ثم افتح: http://localhost:8000/docs

## ميزات
- Subjects/Topics/Questions/Quizzes CRUD مبسّطة
- استيراد CSV: `POST /questions/import` (حقل الملف: `file`)
- توليد شرح AI وهمي مضبوط السلامة: `POST /questions/{id}/explanations/ai` (يتطلب `x-api-key`)
- تخزين SQLite ملفي `medmcq.db`

## شكل CSV
```
subject,topic,stem,option_a,option_b,option_c,option_d,option_e,correct_label,difficulty,source_ref,year
```

## أمان مبسّط
- عمليات الإدارة (إضافة/استيراد/توليد شرح AI) تتطلب ترويسة: `x-api-key: <API_KEY>`

## ملاحظات
- هذا MVP للتجربة السريعة. الإنتاج يحتاج مصادقة كاملة، صلاحيات، وتحسينات.
```
