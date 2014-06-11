-- drop table if exists users;

-- create table users (

--   userid integer primary key autoincrement,

--   username text  not null unique,

--   password text,
--   fname text,
--   lname text,
--   wins integer,
--   loses integer,
--   dateJoined date
-- );

drop table if exists games;

create table games (

  gameid integer primary key autoincrement,
  sets text not null,
  game text,
  dateCreated date,
  started boolean,
  finished boolean
);

drop table if exists userGames;

create table userGames (

  id integer primary key autoincrement,
  userid integer references users(userid),
  gameid integer references game(gameid),
  won boolean,
  score integer
);