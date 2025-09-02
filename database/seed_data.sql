-- Seed data for Landscaper Staff Database
-- This file contains initial data for development and testing

-- Insert sample clients
INSERT INTO clients (company_name, contact_first_name, contact_last_name, email, phone, address_line1, city, state, postal_code, notes) VALUES
('Green Valley Estates', 'John', 'Smith', 'john.smith@greenvalley.com', '555-0101', '123 Oak Street', 'Springfield', 'IL', '62701', 'Large residential development with multiple properties'),
('Downtown Business Center', 'Sarah', 'Johnson', 'sarah.j@downtownbc.com', '555-0102', '456 Business Ave', 'Springfield', 'IL', '62702', 'Commercial property requiring regular maintenance'),
('Smith Family Residence', 'Mike', 'Smith', 'mike.smith@email.com', '555-0103', '789 Garden Lane', 'Springfield', 'IL', '62703', 'Private residence with extensive landscaping needs'),
('Riverside Park District', 'Lisa', 'Davis', 'lisa.davis@riversidepark.org', '555-0104', '321 Park Road', 'Springfield', 'IL', '62704', 'Public park requiring seasonal maintenance'),
('Tech Campus LLC', 'David', 'Wilson', 'd.wilson@techcampus.com', '555-0105', '654 Innovation Drive', 'Springfield', 'IL', '62705', 'Corporate campus with modern landscape design');

-- Insert sample crew members
INSERT INTO crew_members (first_name, last_name, email, phone, role, hire_date, hourly_rate, emergency_contact_name, emergency_contact_phone) VALUES
('John', 'Anderson', 'john.anderson@landscaper.com', '555-0201', 'supervisor', '2023-01-15', 35.00, 'Mary Anderson', '555-0202'),
('Sarah', 'Martinez', 'sarah.martinez@landscaper.com', '555-0203', 'lead', '2023-03-01', 28.00, 'Carlos Martinez', '555-0204'),
('Mike', 'Thompson', 'mike.thompson@landscaper.com', '555-0205', 'operator', '2023-02-10', 22.00, 'Linda Thompson', '555-0206'),
('Emily', 'Rodriguez', 'emily.rodriguez@landscaper.com', '555-0207', 'laborer', '2023-04-15', 18.00, 'Jose Rodriguez', '555-0208'),
('Tom', 'Brown', 'tom.brown@landscaper.com', '555-0209', 'specialist', '2023-01-20', 32.00, 'Susan Brown', '555-0210'),
('Jessica', 'Lee', 'jessica.lee@landscaper.com', '555-0211', 'laborer', '2023-05-01', 18.00, 'Robert Lee', '555-0212');

-- Insert sample materials
INSERT INTO materials (name, material_type, description, length_inches, width_inches, height_inches, weight_lbs, price_per_unit, unit_of_measure, supplier, use_case, installation_notes) VALUES
('Concrete Block 8x8x16', 'block', 'Standard concrete block for retaining walls', 16.00, 8.00, 8.00, 35.00, 2.50, 'each', 'Concrete Supply Co', 'Retaining walls, garden walls', 'Use mortar between blocks, ensure proper drainage'),
('Natural Stone Veneer', 'stone', 'Natural stone for decorative walls', 12.00, 6.00, 2.00, 15.00, 8.75, 'sq ft', 'Stone Works Inc', 'Decorative walls, facades', 'Apply with construction adhesive, seal after installation'),
('Red Clay Brick', 'brick', 'Traditional red clay brick', 8.00, 4.00, 2.25, 4.50, 0.85, 'each', 'Brick & Block Supply', 'Garden walls, walkways', 'Use mortar joints, consider weather sealing'),
('Pressure Treated 4x4', 'wood', 'Pressure treated lumber for posts', 96.00, 4.00, 4.00, 25.00, 12.50, 'each', 'Lumber Yard Plus', 'Fence posts, garden structures', 'Pre-drill holes, use galvanized fasteners'),
('Steel Rebar #4', 'metal', 'Steel reinforcement bar', 240.00, 0.50, 0.50, 2.67, 8.50, 'each', 'Steel Supply Co', 'Concrete reinforcement', 'Cut to length, tie with wire'),
('Decorative Gravel 3/4"', 'stone', 'Decorative gravel for pathways', 0.00, 0.00, 0.00, 0.00, 45.00, 'ton', 'Aggregate Supply', 'Pathways, drainage', 'Install over landscape fabric, compact well'),
('Landscape Fabric', 'other', 'Weed barrier fabric', 0.00, 0.00, 0.00, 0.00, 0.25, 'sq ft', 'Landscape Supply', 'Weed control, soil separation', 'Overlap edges, secure with pins'),
('Concrete Mix 80lb', 'concrete', 'Ready-mix concrete', 0.00, 0.00, 0.00, 80.00, 4.50, 'bag', 'Concrete Supply Co', 'Footings, foundations', 'Mix with water, use within 30 minutes');

-- Insert sample equipment
INSERT INTO equipment (name, equipment_type, brand, model, serial_number, status, purchase_date, purchase_price, current_location, assigned_to, last_maintenance_date, next_maintenance_date) VALUES
('Lawn Mower', 'mower', 'Honda', 'HRX217VKA', 'HM123456', 'available', '2023-01-15', 650.00, 'Truck 1', NULL, '2025-08-15', '2025-09-15'),
('String Trimmer', 'trimmer', 'Stihl', 'FS 56 C-E', 'ST789012', 'in_use', '2023-02-01', 180.00, 'Project PROJ-001', (SELECT id FROM crew_members WHERE first_name = 'Mike' AND last_name = 'Thompson'), '2025-08-10', '2025-11-10'),
('Leaf Blower', 'blower', 'Echo', 'PB-580T', 'EC345678', 'maintenance', '2023-01-20', 220.00, 'Shop', NULL, '2025-08-01', '2025-09-01'),
('Hedge Trimmer', 'trimmer', 'DeWalt', 'DCHT820P1', 'DW901234', 'available', '2023-03-10', 150.00, 'Truck 2', NULL, '2025-07-20', '2025-10-20'),
('Chainsaw', 'saw', 'Husqvarna', '450 Rancher', 'HQ567890', 'available', '2023-02-15', 320.00, 'Truck 1', NULL, '2025-08-05', '2025-11-05'),
('Truck 1', 'vehicle', 'Ford', 'F-250', 'F1234567', 'in_use', '2022-06-01', 45000.00, 'On Site', (SELECT id FROM crew_members WHERE first_name = 'John' AND last_name = 'Anderson'), '2025-07-01', '2025-10-01'),
('Truck 2', 'vehicle', 'Chevrolet', 'Silverado 2500', 'C2345678', 'available', '2022-08-15', 42000.00, 'Shop', NULL, '2025-07-15', '2025-10-15');

-- Insert sample jobs
INSERT INTO jobs (job_number, client_id, title, description, job_type, status, priority, site_address_line1, site_city, site_state, site_postal_code, estimated_start_date, estimated_end_date, estimated_cost, labor_hours_estimated, supervisor_id, lead_worker_id, weather_dependent, special_instructions) VALUES
('PROJ-2025-001', (SELECT id FROM clients WHERE company_name = 'Green Valley Estates'), 'Residential Lawn Renovation', 'Complete lawn renovation with new sod and irrigation system installation', 'lawn_care', 'in_progress', 2, '123 Oak Street', 'Springfield', 'IL', '62701', '2025-08-15', '2025-09-15', 8500.00, 120.00, (SELECT id FROM crew_members WHERE first_name = 'John' AND last_name = 'Anderson'), (SELECT id FROM crew_members WHERE first_name = 'Sarah' AND last_name = 'Martinez'), TRUE, 'Avoid working during rain, coordinate with HOA'),
('PROJ-2025-002', (SELECT id FROM clients WHERE company_name = 'Downtown Business Center'), 'Commercial Landscaping', 'Landscape design and installation for new business center', 'garden_design', 'planning', 1, '456 Business Ave', 'Springfield', 'IL', '62702', '2025-09-01', '2025-09-30', 15000.00, 200.00, (SELECT id FROM crew_members WHERE first_name = 'John' AND last_name = 'Anderson'), (SELECT id FROM crew_members WHERE first_name = 'Tom' AND last_name = 'Brown'), FALSE, 'Work around business hours, coordinate with property manager'),
('PROJ-2025-003', (SELECT id FROM clients WHERE company_name = 'Smith Family Residence'), 'Garden Installation', 'Install new garden beds with native plants and irrigation', 'garden_design', 'completed', 3, '789 Garden Lane', 'Springfield', 'IL', '62703', '2025-07-01', '2025-08-20', 5500.00, 80.00, (SELECT id FROM crew_members WHERE first_name = 'John' AND last_name = 'Anderson'), (SELECT id FROM crew_members WHERE first_name = 'Sarah' AND last_name = 'Martinez'), TRUE, 'Customer prefers native plants only'),
('PROJ-2025-004', (SELECT id FROM clients WHERE company_name = 'Riverside Park District'), 'Fall Cleanup', 'Seasonal cleanup and leaf removal for park areas', 'cleanup', 'planning', 2, '321 Park Road', 'Springfield', 'IL', '62704', '2025-10-01', '2025-10-31', 3200.00, 60.00, (SELECT id FROM crew_members WHERE first_name = 'John' AND last_name = 'Anderson'), (SELECT id FROM crew_members WHERE first_name = 'Mike' AND last_name = 'Thompson'), TRUE, 'Coordinate with park events schedule'),
('PROJ-2025-005', (SELECT id FROM clients WHERE company_name = 'Tech Campus LLC'), 'Tree Services', 'Tree pruning and removal of damaged trees', 'tree_services', 'in_progress', 1, '654 Innovation Drive', 'Springfield', 'IL', '62705', '2025-08-20', '2025-09-10', 4200.00, 45.00, (SELECT id FROM crew_members WHERE first_name = 'John' AND last_name = 'Anderson'), (SELECT id FROM crew_members WHERE first_name = 'Tom' AND last_name = 'Brown'), FALSE, 'Requires traffic control, coordinate with campus security');

-- Insert sample job materials
INSERT INTO job_materials (job_id, material_id, quantity_estimated, unit_cost, notes) VALUES
((SELECT id FROM jobs WHERE job_number = 'PROJ-2025-001'), (SELECT id FROM materials WHERE name = 'Concrete Block 8x8x16'), 200.00, 2.50, 'For retaining wall construction'),
((SELECT id FROM jobs WHERE job_number = 'PROJ-2025-001'), (SELECT id FROM materials WHERE name = 'Landscape Fabric'), 500.00, 0.25, 'Under sod installation'),
((SELECT id FROM jobs WHERE job_number = 'PROJ-2025-002'), (SELECT id FROM materials WHERE name = 'Natural Stone Veneer'), 300.00, 8.75, 'Decorative wall facing'),
((SELECT id FROM jobs WHERE job_number = 'PROJ-2025-002'), (SELECT id FROM materials WHERE name = 'Decorative Gravel 3/4"'), 5.00, 45.00, 'Pathway material'),
((SELECT id FROM jobs WHERE job_number = 'PROJ-2025-003'), (SELECT id FROM materials WHERE name = 'Red Clay Brick'), 150.00, 0.85, 'Garden border'),
((SELECT id FROM jobs WHERE job_number = 'PROJ-2025-003'), (SELECT id FROM materials WHERE name = 'Landscape Fabric'), 200.00, 0.25, 'Weed barrier under plants');

-- Insert sample job crew assignments
INSERT INTO job_crew_assignments (job_id, crew_member_id, role, assigned_date, start_time, end_time, hourly_rate) VALUES
((SELECT id FROM jobs WHERE job_number = 'PROJ-2025-001'), (SELECT id FROM crew_members WHERE first_name = 'John' AND last_name = 'Anderson'), 'Supervisor', '2025-08-15', '07:00', '17:00', 35.00),
((SELECT id FROM jobs WHERE job_number = 'PROJ-2025-001'), (SELECT id FROM crew_members WHERE first_name = 'Sarah' AND last_name = 'Martinez'), 'Lead Worker', '2025-08-15', '07:00', '17:00', 28.00),
((SELECT id FROM jobs WHERE job_number = 'PROJ-2025-001'), (SELECT id FROM crew_members WHERE first_name = 'Mike' AND last_name = 'Thompson'), 'Equipment Operator', '2025-08-15', '07:30', '16:30', 22.00),
((SELECT id FROM jobs WHERE job_number = 'PROJ-2025-001'), (SELECT id FROM crew_members WHERE first_name = 'Emily' AND last_name = 'Rodriguez'), 'Laborer', '2025-08-15', '08:00', '16:00', 18.00),
((SELECT id FROM jobs WHERE job_number = 'PROJ-2025-005'), (SELECT id FROM crew_members WHERE first_name = 'Tom' AND last_name = 'Brown'), 'Tree Specialist', '2025-08-20', '08:00', '16:00', 32.00),
((SELECT id FROM jobs WHERE job_number = 'PROJ-2025-005'), (SELECT id FROM crew_members WHERE first_name = 'Jessica' AND last_name = 'Lee'), 'Ground Support', '2025-08-20', '08:00', '16:00', 18.00);

-- Insert sample job equipment assignments
INSERT INTO job_equipment_assignments (job_id, equipment_id, assigned_date, condition_on_assignment) VALUES
((SELECT id FROM jobs WHERE job_number = 'PROJ-2025-001'), (SELECT id FROM equipment WHERE name = 'String Trimmer'), '2025-08-15', 'Good condition, recently serviced'),
((SELECT id FROM jobs WHERE job_number = 'PROJ-2025-001'), (SELECT id FROM equipment WHERE name = 'Truck 1'), '2025-08-15', 'Good condition, full fuel tank'),
((SELECT id FROM jobs WHERE job_number = 'PROJ-2025-005'), (SELECT id FROM equipment WHERE name = 'Chainsaw'), '2025-08-20', 'Excellent condition, sharp chain'),
((SELECT id FROM jobs WHERE job_number = 'PROJ-2025-005'), (SELECT id FROM equipment WHERE name = 'Truck 2'), '2025-08-20', 'Good condition, clean bed');

-- Insert sample job time entries
INSERT INTO job_time_entries (job_id, crew_member_id, date, start_time, end_time, break_duration_minutes, activity_description) VALUES
((SELECT id FROM jobs WHERE job_number = 'PROJ-2025-001'), (SELECT id FROM crew_members WHERE first_name = 'John' AND last_name = 'Anderson'), '2025-08-15', '07:00', '17:00', 60, 'Site supervision and coordination'),
((SELECT id FROM jobs WHERE job_number = 'PROJ-2025-001'), (SELECT id FROM crew_members WHERE first_name = 'Sarah' AND last_name = 'Martinez'), '2025-08-15', '07:00', '17:00', 60, 'Retaining wall construction'),
((SELECT id FROM jobs WHERE job_number = 'PROJ-2025-001'), (SELECT id FROM crew_members WHERE first_name = 'Mike' AND last_name = 'Thompson'), '2025-08-15', '07:30', '16:30', 60, 'Equipment operation and site prep'),
((SELECT id FROM jobs WHERE job_number = 'PROJ-2025-001'), (SELECT id FROM crew_members WHERE first_name = 'Emily' AND last_name = 'Rodriguez'), '2025-08-15', '08:00', '16:00', 30, 'Material handling and cleanup'),
((SELECT id FROM jobs WHERE job_number = 'PROJ-2025-005'), (SELECT id FROM crew_members WHERE first_name = 'Tom' AND last_name = 'Brown'), '2025-08-20', '08:00', '16:00', 60, 'Tree pruning and removal'),
((SELECT id FROM jobs WHERE job_number = 'PROJ-2025-005'), (SELECT id FROM crew_members WHERE first_name = 'Jessica' AND last_name = 'Lee'), '2025-08-20', '08:00', '16:00', 30, 'Ground support and cleanup');

-- Update equipment status based on assignments
UPDATE equipment SET status = 'in_use', assigned_to = (SELECT id FROM crew_members WHERE first_name = 'Mike' AND last_name = 'Thompson') WHERE name = 'String Trimmer';
UPDATE equipment SET status = 'in_use', assigned_to = (SELECT id FROM crew_members WHERE first_name = 'John' AND last_name = 'Anderson') WHERE name = 'Truck 1';
UPDATE equipment SET status = 'in_use', assigned_to = (SELECT id FROM crew_members WHERE first_name = 'Tom' AND last_name = 'Brown') WHERE name = 'Chainsaw';
UPDATE equipment SET status = 'in_use', assigned_to = (SELECT id FROM crew_members WHERE first_name = 'Tom' AND last_name = 'Brown') WHERE name = 'Truck 2';
