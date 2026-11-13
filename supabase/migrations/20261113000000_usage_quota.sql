-- Compteur d'usage quotidien par utilisateur (identifiant RevenueCat anonyme).
-- Ne contient AUCUN contenu de conversation.
create table if not exists public.daily_usage (
  user_id text not null,
  day date not null default (now() at time zone 'utc')::date,
  count integer not null default 0 check (count >= 0),
  primary key (user_id, day)
);

-- Accès réservé au serveur (service_role) : RLS activée sans aucune politique.
alter table public.daily_usage enable row level security;
revoke all on public.daily_usage from anon, authenticated;

-- Incrémente atomiquement et renvoie false si la limite est atteinte.
create or replace function public.consume_quota(p_user_id text, p_limit integer)
returns boolean
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_count integer;
begin
  insert into public.daily_usage as u (user_id, day, count)
  values (p_user_id, (now() at time zone 'utc')::date, 1)
  on conflict (user_id, day)
    do update set count = u.count + 1
    where u.count < p_limit
  returning u.count into v_count;

  return v_count is not null;
end;
$$;

revoke all on function public.consume_quota(text, integer) from public, anon, authenticated;
grant execute on function public.consume_quota(text, integer) to service_role;

-- Purge : à planifier (pg_cron) pour ne garder que 7 jours de compteurs.
create or replace function public.purge_daily_usage()
returns void
language sql
security definer
set search_path = ''
as $$
  delete from public.daily_usage where day < (now() at time zone 'utc')::date - 7;
$$;

revoke all on function public.purge_daily_usage() from public, anon, authenticated;
