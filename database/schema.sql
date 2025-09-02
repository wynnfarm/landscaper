-- Landscaper Staff Database Schema
-- PostgreSQL Database Design for Landscape Management System

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create custom types
CREATE TYPE job_status AS ENUM ('planning', 'in_progress', 'on_hold', 'completed', 'cancelled');
CREATE TYPE material_type AS ENUM ('block', 'stone', 'brick', 'concrete', 'wood', 'metal', 'other');
CREATE TYPE equipment_status AS ENUM ('available', 'in_use', 'maintenance', 'retired');
CREATE TYPE crew_role AS ENUM ('supervisor', 'lead', 'operator', 'laborer', 'specialist');

-- Clients table
CREATE TABLE clients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_name VARCHAR(255),
    contact_first_name VARCHAR(100) NOT NULL,
    contact_last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    country VARCHAR(100) DEFAULT 'USA',
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Materials table
CREATE TABLE materials (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    material_type material_type NOT NULL,
    description TEXT,
    length_inches DECIMAL(8,2),
    width_inches DECIMAL(8,2),
    height_inches DECIMAL(8,2),
    weight_lbs DECIMAL(8,2),
    price_per_unit DECIMAL(10,2) NOT NULL,
    unit_of_measure VARCHAR(50) DEFAULT 'each',
    supplier VARCHAR(255),
    supplier_part_number VARCHAR(100),
    use_case TEXT,
    installation_notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Crew members table
CREATE TABLE crew_members (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    role crew_role NOT NULL,
    hire_date DATE,
    hourly_rate DECIMAL(8,2),
    is_active BOOLEAN DEFAULT TRUE,
    emergency_contact_name VARCHAR(255),
    emergency_contact_phone VARCHAR(20),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Equipment table
CREATE TABLE equipment (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    equipment_type VARCHAR(100) NOT NULL,
    brand VARCHAR(100),
    model VARCHAR(100),
    serial_number VARCHAR(100),
    status equipment_status DEFAULT 'available',
    purchase_date DATE,
    purchase_price DECIMAL(10,2),
    current_location VARCHAR(255),
    assigned_to UUID REFERENCES crew_members(id),
    last_maintenance_date DATE,
    next_maintenance_date DATE,
    maintenance_notes TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Jobs table (main project table)
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_number VARCHAR(50) UNIQUE NOT NULL,
    client_id UUID NOT NULL REFERENCES clients(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    job_type VARCHAR(100) NOT NULL, -- 'lawn_care', 'tree_services', 'garden_design', 'cleanup', 'maintenance'
    status job_status DEFAULT 'planning',
    priority INTEGER DEFAULT 3, -- 1=high, 2=medium, 3=low
    
    -- Location information
    site_address_line1 VARCHAR(255),
    site_address_line2 VARCHAR(255),
    site_city VARCHAR(100),
    site_state VARCHAR(50),
    site_postal_code VARCHAR(20),
    site_notes TEXT,
    
    -- Scheduling
    estimated_start_date DATE,
    estimated_end_date DATE,
    actual_start_date DATE,
    actual_end_date DATE,
    
    -- Financial
    estimated_cost DECIMAL(12,2),
    actual_cost DECIMAL(12,2),
    labor_hours_estimated DECIMAL(8,2),
    labor_hours_actual DECIMAL(8,2),
    
    -- Project management
    supervisor_id UUID REFERENCES crew_members(id),
    lead_worker_id UUID REFERENCES crew_members(id),
    
    -- Additional fields
    weather_dependent BOOLEAN DEFAULT FALSE,
    requires_permits BOOLEAN DEFAULT FALSE,
    permit_numbers TEXT,
    special_instructions TEXT,
    completion_notes TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES crew_members(id)
);

-- Job materials (many-to-many relationship)
CREATE TABLE job_materials (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    material_id UUID NOT NULL REFERENCES materials(id),
    quantity_estimated DECIMAL(10,2) NOT NULL,
    quantity_actual DECIMAL(10,2),
    unit_cost DECIMAL(10,2) NOT NULL,
    total_cost DECIMAL(12,2) GENERATED ALWAYS AS (quantity_estimated * unit_cost) STORED,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(job_id, material_id)
);

-- Job crew assignments
CREATE TABLE job_crew_assignments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    crew_member_id UUID NOT NULL REFERENCES crew_members(id),
    role VARCHAR(100) NOT NULL,
    assigned_date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    hours_worked DECIMAL(4,2),
    hourly_rate DECIMAL(8,2),
    total_cost DECIMAL(10,2) GENERATED ALWAYS AS (COALESCE(hours_worked, 0) * COALESCE(hourly_rate, 0)) STORED,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(job_id, crew_member_id, assigned_date)
);

-- Job equipment assignments
CREATE TABLE job_equipment_assignments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    equipment_id UUID NOT NULL REFERENCES equipment(id),
    assigned_date DATE NOT NULL,
    returned_date DATE,
    condition_on_assignment TEXT,
    condition_on_return TEXT,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Job photos/documents
CREATE TABLE job_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_size INTEGER,
    document_type VARCHAR(100), -- 'before_photo', 'after_photo', 'progress_photo', 'invoice', 'permit', 'other'
    description TEXT,
    uploaded_by UUID REFERENCES crew_members(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Job time tracking
CREATE TABLE job_time_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    crew_member_id UUID NOT NULL REFERENCES crew_members(id),
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME,
    break_duration_minutes INTEGER DEFAULT 0,
    total_hours DECIMAL(4,2) GENERATED ALWAYS AS (
        CASE 
            WHEN end_time IS NOT NULL THEN 
                EXTRACT(EPOCH FROM (end_time - start_time)) / 3600 - (break_duration_minutes / 60.0)
            ELSE 0
        END
    ) STORED,
    activity_description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX idx_jobs_client_id ON jobs(client_id);
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_estimated_start_date ON jobs(estimated_start_date);
CREATE INDEX idx_jobs_supervisor_id ON jobs(supervisor_id);
CREATE INDEX idx_job_materials_job_id ON job_materials(job_id);
CREATE INDEX idx_job_materials_material_id ON job_materials(material_id);
CREATE INDEX idx_job_crew_assignments_job_id ON job_crew_assignments(job_id);
CREATE INDEX idx_job_crew_assignments_crew_member_id ON job_crew_assignments(crew_member_id);
CREATE INDEX idx_job_equipment_assignments_job_id ON job_equipment_assignments(job_id);
CREATE INDEX idx_job_equipment_assignments_equipment_id ON job_equipment_assignments(equipment_id);
CREATE INDEX idx_job_documents_job_id ON job_documents(job_id);
CREATE INDEX idx_job_time_entries_job_id ON job_time_entries(job_id);
CREATE INDEX idx_job_time_entries_crew_member_id ON job_time_entries(crew_member_id);
CREATE INDEX idx_job_time_entries_date ON job_time_entries(date);
CREATE INDEX idx_equipment_status ON equipment(status);
CREATE INDEX idx_equipment_assigned_to ON equipment(assigned_to);
CREATE INDEX idx_crew_members_role ON crew_members(role);
CREATE INDEX idx_crew_members_is_active ON crew_members(is_active);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_clients_updated_at BEFORE UPDATE ON clients FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_materials_updated_at BEFORE UPDATE ON materials FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_crew_members_updated_at BEFORE UPDATE ON crew_members FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_equipment_updated_at BEFORE UPDATE ON equipment FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_jobs_updated_at BEFORE UPDATE ON jobs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_job_materials_updated_at BEFORE UPDATE ON job_materials FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_job_crew_assignments_updated_at BEFORE UPDATE ON job_crew_assignments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_job_equipment_assignments_updated_at BEFORE UPDATE ON job_equipment_assignments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_job_time_entries_updated_at BEFORE UPDATE ON job_time_entries FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
