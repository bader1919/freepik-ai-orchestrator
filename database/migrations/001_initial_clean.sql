-- Freepik AI Orchestrator Database Schema
-- Clean, human-readable version

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Core task tracking
CREATE TABLE freepik_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id VARCHAR(255) UNIQUE NOT NULL,
    user_input TEXT NOT NULL,
    enhanced_prompt TEXT,
    model_used VARCHAR(50) NOT NULL,
    source VARCHAR(50) NOT NULL,
    task_type VARCHAR(50) DEFAULT 'generation',
    environment VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    result_url TEXT,
    thumbnail_url TEXT,
    error_message TEXT,
    optimization_data JSONB,
    workflow_id VARCHAR(100),
    user_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    processing_time_seconds INTEGER
);

-- Workflow templates
CREATE TABLE workflows (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    steps JSONB NOT NULL,
    user_id VARCHAR(100),
    is_custom BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- User analytics and metrics
CREATE TABLE user_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    generations_count INTEGER DEFAULT 0,
    successful_generations INTEGER DEFAULT 0,
    failed_generations INTEGER DEFAULT 0,
    total_cost_cents INTEGER DEFAULT 0,
    models_used JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, date)
);

-- Performance indexes
CREATE INDEX idx_freepik_tasks_task_id ON freepik_tasks(task_id);
CREATE INDEX idx_freepik_tasks_status ON freepik_tasks(status);
CREATE INDEX idx_freepik_tasks_user_id ON freepik_tasks(user_id);
CREATE INDEX idx_freepik_tasks_created_at ON freepik_tasks(created_at);
CREATE INDEX idx_workflows_user_id ON workflows(user_id);
CREATE INDEX idx_user_analytics_user_date ON user_analytics(user_id, date);

-- Default workflow templates
INSERT INTO workflows (workflow_id, name, description, steps, is_custom) VALUES
('professional_headshot', 'Professional Headshot', 'High-quality professional headshots with optimal lighting',
 '[{"action": "generate", "model": "imagen3", "params": {"style": "professional_photography"}},
   {"action": "relight", "params": {"lighting": "professional_portrait"}},
   {"action": "upscale", "params": {"factor": 4}},
   {"action": "variants", "params": {"count": 3, "variation_type": "lighting"}}]', false),

('product_photography', 'Product Photography', 'E-commerce ready product images with multiple angles',
 '[{"action": "generate", "model": "imagen3", "params": {"style": "product_photography"}},
   {"action": "remove_background"},
   {"action": "relight", "params": {"lighting": "studio"}},
   {"action": "variants", "params": {"count": 4, "variation_type": "angle"}},
   {"action": "upscale", "params": {"factor": 4}}]', false),

('marketing_materials', 'Marketing Materials', 'Social media and marketing content with brand consistency',
 '[{"action": "generate", "model": "mystic", "params": {"style": "marketing"}},
   {"action": "style_variants", "params": {"styles": ["modern", "classic", "bold"]}},
   {"action": "aspect_ratio_variants", "params": {"ratios": ["16:9", "1:1", "9:16"]}},
   {"action": "brand_overlay", "params": {"overlay_type": "logo"}}]', false);
