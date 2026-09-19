-- Workapp jobs table. Run this in Supabase > SQL Editor.
create table if not exists jobs (
  id bigint generated always as identity primary key,
  title text not null,
  company_name text default '',
  location text default '',
  description text default '',
  url text default '' unique,
  source text default '',
  salary text default '',
  posted_at text default '',
  email text default '',
  company_website text default '',
  job_type text default 'unknown',
  modality text default 'unknown',
  created_at timestamptz default now()
);

-- Allow the anon/service key used by the app to read + upsert.
alter table jobs enable row level security;
grant select, insert, update, delete on public.jobs to anon, authenticated;
drop policy if exists "jobs_read_all" on jobs;
drop policy if exists "jobs_write_all" on jobs;
create policy "jobs_read_all" on jobs for select using (true);
create policy "jobs_write_all" on jobs for insert with check (true);
create policy "jobs_update_all" on jobs for update using (true) with check (true);

create index if not exists jobs_source_idx on jobs (source);
create index if not exists jobs_created_idx on jobs (created_at desc);
