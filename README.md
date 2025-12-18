# GIVC Core Academy

<div dir="rtl" lang="ar">

## أكاديمية GIVC الأساسية
منصة تدريب شاملة للتأمين الصحي والترميز الطبي في المملكة العربية السعودية

</div>

---

## Overview

GIVC Core Academy is a comprehensive Saudi healthcare insurance and medical coding training platform. It provides specialized training in ICD-10-AM, SBS (Saudi Billing System), and AR-DRG coding systems with support for multiple training modalities.

For the updated SBS-centric architecture, compliance scope, and phased rollout, see **[SBS_CENTRIC_BLUEPRINT.md](./SBS_CENTRIC_BLUEPRINT.md)**.

### Key Features

- 🎓 **Multi-Modal Training**: Virtual Live, Self-Paced, Bootcamp, and Blended learning
- 🏥 **Saudi-Specific Coding**: ICD-10-AM-SA, SBS, AR-DRG systems
- 🔐 **Secure Authentication**: JWT with MFA support for privileged roles
- 💳 **Flexible Pricing**: 4 subscription tiers (Basic, Standard, Premium, Corporate)
- 🌍 **Bilingual Support**: Arabic-first with RTL layout and English support
- 📊 **Analytics Dashboard**: Per-segment metrics for learners and corporate accounts
- ✅ **Compliance Ready**: HIPAA and NPHIES patterns, full audit logging
- 🤖 **AI-Powered**: Adaptive learning recommendations and personalized study paths

---

## Technical Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **ORM**: SQLAlchemy with Pydantic V2
- **Database**: PostgreSQL 15+ (production), SQLite (development)
- **Caching**: Redis 7+
- **Task Queue**: Celery
- **Authentication**: JWT with MFA support

### Frontend
- **Framework**: Next.js 14 (App Router)
- **UI**: React 18, TypeScript, Tailwind CSS
- **Components**: Radix UI, Shadcn/ui
- **State**: Zustand, React Query
- **i18n**: react-i18next with RTL support

### Mobile
- **Framework**: React Native + Expo (iOS/Android)

---

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 20+ (for local development)
- Python 3.11+ (for local development)

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/Fadil369/givc-core-academy.git
cd givc-core-academy

# Run setup script
chmod +x setup.sh
./setup.sh

# Services will be available at:
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/api/docs
# - Frontend: http://localhost:3000
```

### Local Development

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python scripts/seed_data.py

# Start the server
uvicorn app.main:app --reload

# Run tests
pytest --cov=app tests/
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

#### Mobile

```bash
cd mobile

# Install dependencies
npm install

# Start Expo development server
npm start

# Run on iOS
npm run ios

# Run on Android
npm run android
```

---

## Project Structure

```
givc-core-academy/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # API endpoints
│   │   ├── core/            # Security & dependencies
│   │   ├── models/          # Database models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   ├── config.py        # Configuration
│   │   ├── database.py      # Database setup
│   │   └── main.py          # FastAPI app
│   ├── scripts/             # Utility scripts
│   ├── tests/               # Test suite
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/             # Next.js app router
│   │   ├── components/      # React components
│   │   ├── lib/             # Utilities
│   │   └── i18n/            # Internationalization
│   ├── package.json
│   └── Dockerfile
├── mobile/
│   ├── src/                 # React Native source
│   ├── App.tsx              # Main app component
│   └── package.json
├── docker-compose.yml       # Container orchestration
├── setup.sh                 # Setup script
└── README.md
```

---

## API Documentation

Once the backend is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### Sample API Endpoints

- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/courses` - List courses
- `POST /api/v1/enrollments` - Enroll in course
- `GET /api/v1/assessments/course/{id}` - Get course assessments
- `POST /api/v1/payments/create-payment-intent` - Create payment

---

## Subscription Tiers

| Tier | Price (SAR) | Features |
|------|-------------|----------|
| **Basic** | 2,000-3,000 | Self-paced content, limited question bank |
| **Standard** | 5,000-7,000 | + Simulators, recorded sessions |
| **Premium** | 8,000-12,000 | + Live training, personal instructor |
| **Corporate** | Custom | + Custom platform, admin reports, bulk enrollment |

*All prices include 15% VAT*

---

## Testing

### Backend Tests

```bash
cd backend
pytest --cov=app tests/
```

Target coverage: >80%

### Frontend Tests

```bash
cd frontend
npm test
```

---

## Sample Credentials

After running the seed script, use these credentials:

- **Admin**: admin@givc.sa / admin123
- **Student**: student@example.com / student123

---

## Saudi-Specific Features

### Regulatory Bodies
- CHI (Council of Health Insurance)
- SCFHS (Saudi Commission for Health Specialties)
- MOH (Ministry of Health)
- SFDA (Saudi Food and Drug Authority)

### Coding Systems
- **ICD-10-AM-SA**: International Classification of Diseases
- **SBS**: Saudi Billing System
- **AR-DRG**: Arabic Refined Diagnosis Related Groups

### Compliance
- Saudi National ID / Iqama validation
- Currency: SAR with 15% VAT
- Arabic-first interface with RTL support
- PHI encryption (AES-256 at rest, TLS 1.3 in transit)

---

## Environment Variables

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=postgresql://givc:givc123@localhost:5432/givc_academy

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Security
SECRET_KEY=your-secret-key-here

# Stripe
STRIPE_API_KEY=your-stripe-key
STRIPE_WEBHOOK_SECRET=your-webhook-secret

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License.

---

## Support

For support and inquiries:
- Email: support@givc.sa
- Documentation: [API Docs](http://localhost:8000/api/docs)

---

<div dir="rtl" lang="ar">

## الدعم الفني

للدعم والاستفسارات:
- البريد الإلكتروني: support@givc.sa
- الوثائق: [مستندات API](http://localhost:8000/api/docs)

</div>
