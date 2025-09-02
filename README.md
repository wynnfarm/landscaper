# Landscaper Staff Dashboard

A comprehensive staff management system for landscaping companies, built with Flask and PostgreSQL. This application provides tools for project management, crew coordination, equipment tracking, and materials calculation.

## Features

### 🏠 **Staff Dashboard**

- Overview of active projects, crew status, and equipment
- Quick access to all tools and resources
- Real-time status updates

### 📋 **Project Management**

- Track active and completed projects
- Project status updates and timeline management
- Client information and site details
- Cost estimation and tracking

### 👥 **Crew Management**

- Staff schedules and assignments
- Contact information and emergency contacts
- Role-based access and permissions
- Time tracking and payroll integration

### 🔧 **Equipment & Tools**

- Equipment status tracking (Available/In Use/Maintenance)
- Maintenance schedules and history
- Location tracking and assignments
- Issue reporting and repair tracking

### 🧮 **Materials Calculator**

- Wall material calculations
- Cost estimation and material lists
- Integration with project planning
- Supplier and inventory management

### 🤖 **AI Assistant**

- Intelligent landscaping advice
- Context-aware responses
- Integration with MCP (Model Context Protocol)
- Project-specific recommendations

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Containerization**: Docker
- **AI Integration**: MCP (Context Manager & Persona Manager)

## Database Schema

The application uses a comprehensive PostgreSQL database with the following main entities:

- **Clients**: Customer information and contact details
- **Jobs**: Project management and tracking
- **Crew Members**: Staff information and roles
- **Equipment**: Tools and machinery tracking
- **Materials**: Inventory and pricing
- **Job Materials**: Material usage tracking
- **Job Crew Assignments**: Staff scheduling
- **Job Equipment Assignments**: Equipment allocation
- **Job Time Entries**: Time tracking and payroll

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Git

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Git

### 1. Clone the Repository

```bash
git clone <repository-url>
cd landscaper
```

### 2. Set Up Environment Variables

**⚠️ IMPORTANT: Security Setup Required**

Create a `.env` file in the project root with your secure credentials:

```bash
cp env.example .env
```

Then edit `.env` with your secure passwords and keys:

```bash
# Database Configuration
POSTGRES_PASSWORD=your_secure_postgres_password_here
DB_PASSWORD=your_secure_db_password_here

# Application Security
SECRET_KEY=your_secure_secret_key_here

# pgAdmin Configuration (for development)
PGADMIN_PASSWORD=your_secure_pgadmin_password_here
```

**Never commit the `.env` file to version control!**

### 3. Start the Database

```bash
# Start PostgreSQL and Redis containers
docker-compose up -d landscaper-db landscaper-redis

# Wait for database to be ready (about 30 seconds)
docker-compose logs -f landscaper-db
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize the Database

```bash
# Run the database initialization script
python database/init_db.py
```

### 5. Start the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Docker Setup

### Full Stack with Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Database Only

```bash
# Start just the database
docker-compose up -d landscaper-db

# Access database directly
docker exec -it landscaper-database psql -U landscaper_user -d landscaper
```

### Development with pgAdmin

```bash
# Start database and pgAdmin
docker-compose --profile development up -d

# Access pgAdmin at http://localhost:8080
# Email: admin@landscaper.local
# Password: admin123
```

## Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=landscaper
DB_USER=landscaper_user
DB_PASSWORD=landscaper_password_2024

# Flask Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
PORT=5000

# Redis Configuration (optional)
REDIS_URL=redis://localhost:6379/0
```

## API Endpoints

### Projects

- `GET /projects` - List all projects
- `POST /api/project/update` - Update project status

### Crew Management

- `GET /crew` - List crew members and schedules
- `GET /api/crew/status` - Get crew status

### Equipment

- `GET /tools` - List equipment and tools
- `GET /api/equipment/status` - Get equipment status

### Materials

- `GET /api/materials` - List all materials
- `POST /api/calculate-materials` - Calculate material requirements

### AI Chat

- `POST /api/chat` - Send message to AI assistant
- `GET /api/agent/status` - Get AI agent status

## Database Management

### Backup Database

```bash
# Create backup
docker exec landscaper-database pg_dump -U landscaper_user landscaper > backup.sql

# Restore backup
docker exec -i landscaper-database psql -U landscaper_user landscaper < backup.sql
```

### Reset Database

```bash
# Stop and remove database container
docker-compose down landscaper-db

# Remove database volume
docker volume rm landscaper_postgres_data

# Restart and reinitialize
docker-compose up -d landscaper-db
python database/init_db.py
```

## Development

### Project Structure

```
landscaper/
├── app.py                 # Main Flask application
├── models/               # Database models
│   ├── __init__.py
│   ├── base.py
│   ├── client.py
│   ├── job.py
│   ├── crew_member.py
│   ├── equipment.py
│   └── ...
├── templates/            # HTML templates
├── static/              # CSS, JS, images
├── database/            # Database scripts
│   ├── schema.sql
│   ├── seed_data.sql
│   └── init_db.py
├── mcp_integration/     # AI integration
├── docker-compose.yml   # Docker configuration
└── requirements.txt     # Python dependencies
```

### Adding New Features

1. **Database Changes**: Update `database/schema.sql` and run migrations
2. **Models**: Add new models in `models/` directory
3. **Routes**: Add new routes in `app.py`
4. **Templates**: Create new templates in `templates/`
5. **API**: Add new API endpoints for data access

### Testing

```bash
# Run basic tests
python test_calculator.py

# Test database connection
python -c "from models.base import init_database; from app import app; init_database(app); print('Database connected successfully')"
```

## Production Deployment

### Using Gunicorn

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Environment Configuration

For production, set these environment variables:

```env
DEBUG=False
SECRET_KEY=your-production-secret-key
DB_HOST=your-production-db-host
DB_PASSWORD=your-production-db-password
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:

- Create an issue in the repository
- Check the documentation
- Review the database schema in `database/schema.sql`

## Roadmap

- [ ] Mobile app development
- [ ] Advanced reporting and analytics
- [ ] Integration with accounting software
- [ ] GPS tracking for equipment
- [ ] Weather API integration
- [ ] Customer portal
- [ ] Inventory management system
- [ ] Automated scheduling
