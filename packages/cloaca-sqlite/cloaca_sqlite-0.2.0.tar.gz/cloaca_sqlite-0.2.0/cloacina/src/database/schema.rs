/*
 *  Copyright 2025 Colliery Software
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

// Schema selection based on backend feature flags

#[cfg(feature = "postgres")]
mod postgres_schema {
    // PostgreSQL schema using native types
    diesel::table! {
        contexts (id) {
            id -> Uuid,
            value -> Varchar,
            created_at -> Timestamp,
            updated_at -> Timestamp,
        }
    }

    diesel::table! {
        pipeline_executions (id) {
            id -> Uuid,
            pipeline_name -> Varchar,
            pipeline_version -> Varchar,
            status -> Varchar,
            context_id -> Nullable<Uuid>,
            started_at -> Timestamp,
            completed_at -> Nullable<Timestamp>,
            error_details -> Nullable<Text>,
            recovery_attempts -> Int4,
            last_recovery_at -> Nullable<Timestamp>,
            created_at -> Timestamp,
            updated_at -> Timestamp,
        }
    }

    diesel::table! {
        task_executions (id) {
            id -> Uuid,
            pipeline_execution_id -> Uuid,
            task_name -> Varchar,
            status -> Varchar,
            started_at -> Nullable<Timestamp>,
            completed_at -> Nullable<Timestamp>,
            attempt -> Int4,
            max_attempts -> Int4,
            error_details -> Nullable<Text>,
            trigger_rules -> Text,
            task_configuration -> Text,
            retry_at -> Nullable<Timestamp>,
            last_error -> Nullable<Text>,
            recovery_attempts -> Int4,
            last_recovery_at -> Nullable<Timestamp>,
            created_at -> Timestamp,
            updated_at -> Timestamp,
        }
    }

    diesel::table! {
        recovery_events (id) {
            id -> Uuid,
            pipeline_execution_id -> Uuid,
            task_execution_id -> Nullable<Uuid>,
            recovery_type -> Varchar,
            recovered_at -> Timestamp,
            details -> Nullable<Text>,
            created_at -> Timestamp,
            updated_at -> Timestamp,
        }
    }

    diesel::table! {
        task_execution_metadata (id) {
            id -> Uuid,
            task_execution_id -> Uuid,
            pipeline_execution_id -> Uuid,
            task_name -> Varchar,
            context_id -> Nullable<Uuid>,
            created_at -> Timestamp,
            updated_at -> Timestamp,
        }
    }

    diesel::table! {
        workflow_registry (id) {
            id -> Uuid,
            created_at -> Timestamp,
            data -> Bytea,
        }
    }

    diesel::table! {
        workflow_packages (id) {
            id -> Uuid,
            registry_id -> Uuid,
            package_name -> Varchar,
            version -> Varchar,
            description -> Nullable<Text>,
            author -> Nullable<Varchar>,
            metadata -> Text,
            created_at -> Timestamp,
            updated_at -> Timestamp,
        }
    }

    diesel::table! {
        cron_schedules (id) {
            id -> Uuid,
            workflow_name -> Varchar,
            cron_expression -> Varchar,
            timezone -> Varchar,
            enabled -> Bool,
            catchup_policy -> Varchar,
            start_date -> Nullable<Timestamp>,
            end_date -> Nullable<Timestamp>,
            next_run_at -> Timestamp,
            last_run_at -> Nullable<Timestamp>,
            created_at -> Timestamp,
            updated_at -> Timestamp,
        }
    }

    diesel::table! {
        cron_executions (id) {
            id -> Uuid,
            schedule_id -> Uuid,
            pipeline_execution_id -> Nullable<Uuid>,
            scheduled_time -> Timestamp,
            claimed_at -> Timestamp,
            created_at -> Timestamp,
            updated_at -> Timestamp,
        }
    }

    diesel::joinable!(pipeline_executions -> contexts (context_id));
    diesel::joinable!(task_executions -> pipeline_executions (pipeline_execution_id));
    diesel::joinable!(task_execution_metadata -> task_executions (task_execution_id));
    diesel::joinable!(task_execution_metadata -> pipeline_executions (pipeline_execution_id));
    diesel::joinable!(task_execution_metadata -> contexts (context_id));
    diesel::joinable!(recovery_events -> pipeline_executions (pipeline_execution_id));
    diesel::joinable!(recovery_events -> task_executions (task_execution_id));
    diesel::joinable!(cron_executions -> cron_schedules (schedule_id));
    diesel::joinable!(cron_executions -> pipeline_executions (pipeline_execution_id));
    diesel::joinable!(workflow_packages -> workflow_registry (registry_id));

    diesel::allow_tables_to_appear_in_same_query!(
        contexts,
        cron_executions,
        cron_schedules,
        pipeline_executions,
        recovery_events,
        task_executions,
        task_execution_metadata,
        workflow_packages,
        workflow_registry,
    );
}

#[cfg(feature = "sqlite")]
mod sqlite_schema {
    // SQLite schema with appropriate type mappings
    diesel::table! {
        contexts (id) {
            id -> Binary,
            value -> Text,
            created_at -> Text,
            updated_at -> Text,
        }
    }

    diesel::table! {
        pipeline_executions (id) {
            id -> Binary,
            pipeline_name -> Text,
            pipeline_version -> Text,
            status -> Text,
            context_id -> Nullable<Binary>,
            started_at -> Text,
            completed_at -> Nullable<Text>,
            error_details -> Nullable<Text>,
            recovery_attempts -> Integer,
            last_recovery_at -> Nullable<Text>,
            created_at -> Text,
            updated_at -> Text,
        }
    }

    diesel::table! {
        task_executions (id) {
            id -> Binary,
            pipeline_execution_id -> Binary,
            task_name -> Text,
            status -> Text,
            started_at -> Nullable<Text>,
            completed_at -> Nullable<Text>,
            attempt -> Integer,
            max_attempts -> Integer,
            error_details -> Nullable<Text>,
            trigger_rules -> Text,
            task_configuration -> Text,
            retry_at -> Nullable<Text>,
            last_error -> Nullable<Text>,
            recovery_attempts -> Integer,
            last_recovery_at -> Nullable<Text>,
            created_at -> Text,
            updated_at -> Text,
        }
    }

    diesel::table! {
        recovery_events (id) {
            id -> Binary,
            pipeline_execution_id -> Binary,
            task_execution_id -> Nullable<Binary>,
            recovery_type -> Text,
            recovered_at -> Text,
            details -> Nullable<Text>,
            created_at -> Text,
            updated_at -> Text,
        }
    }

    diesel::table! {
        task_execution_metadata (id) {
            id -> Binary,
            task_execution_id -> Binary,
            pipeline_execution_id -> Binary,
            task_name -> Text,
            context_id -> Nullable<Binary>,
            created_at -> Text,
            updated_at -> Text,
        }
    }

    diesel::table! {
        workflow_registry (id) {
            id -> Binary,
            created_at -> Text,
            data -> Binary,
        }
    }

    diesel::table! {
        workflow_packages (id) {
            id -> Binary,
            registry_id -> Binary,
            package_name -> Text,
            version -> Text,
            description -> Nullable<Text>,
            author -> Nullable<Text>,
            metadata -> Text,
            created_at -> Text,
            updated_at -> Text,
        }
    }

    diesel::table! {
        cron_schedules (id) {
            id -> Binary,
            workflow_name -> Text,
            cron_expression -> Text,
            timezone -> Text,
            enabled -> Integer,
            catchup_policy -> Text,
            start_date -> Nullable<Text>,
            end_date -> Nullable<Text>,
            next_run_at -> Text,
            last_run_at -> Nullable<Text>,
            created_at -> Text,
            updated_at -> Text,
        }
    }

    diesel::table! {
        cron_executions (id) {
            id -> Binary,
            schedule_id -> Binary,
            pipeline_execution_id -> Nullable<Binary>,
            scheduled_time -> Text,
            claimed_at -> Text,
            created_at -> Text,
            updated_at -> Text,
        }
    }

    diesel::joinable!(pipeline_executions -> contexts (context_id));
    diesel::joinable!(task_executions -> pipeline_executions (pipeline_execution_id));
    diesel::joinable!(task_execution_metadata -> task_executions (task_execution_id));
    diesel::joinable!(task_execution_metadata -> pipeline_executions (pipeline_execution_id));
    diesel::joinable!(task_execution_metadata -> contexts (context_id));
    diesel::joinable!(recovery_events -> pipeline_executions (pipeline_execution_id));
    diesel::joinable!(recovery_events -> task_executions (task_execution_id));
    diesel::joinable!(cron_executions -> cron_schedules (schedule_id));
    diesel::joinable!(cron_executions -> pipeline_executions (pipeline_execution_id));

    diesel::allow_tables_to_appear_in_same_query!(
        contexts,
        cron_executions,
        cron_schedules,
        pipeline_executions,
        recovery_events,
        task_executions,
        task_execution_metadata,
    );
}

// Re-export the appropriate schema based on feature flags
#[cfg(all(feature = "postgres", not(feature = "sqlite")))]
pub use postgres_schema::*;

#[cfg(all(feature = "sqlite", not(feature = "postgres")))]
pub use sqlite_schema::*;
