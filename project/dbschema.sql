drop table if exists projects;
create table projects (
  id integer primary key autoincrement,
  projectname text not null,
  technology text not null
);