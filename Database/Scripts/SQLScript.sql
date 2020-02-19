
-- Считаем общее количество зарегестрированных навыков
select count(*) from skills;

-- Считаем общее количество найденных вакансий
select count(*) from vacancies;

-- Считаем вакансии, где указана зарплат
select count(*) from vacancies where max_salary is not null or min_salary is not null;

-- Считаем вакансии, где зарплата не указана
select count(*) from vacancies where max_salary is null and min_salary is null;

-- Считаем количество регионов
select count(*) from regions;

-- Считаем колво вакансий в каждом регионе
select count(*),r.city from regions r, vacancies v where  r.id == v.region_id group by r.id;

-- Считаем кол-во навыков для вакансий
select v.name, v.id, count(s.skills_id) from vacancies v, skills_vacancies s where v.id == s.vacancy_id group by v.id;

-- Выводим список навыков для каждой вакансии
select v.name, s.name from vacancies v, skills_vacancies vs, skills s where v.id == vs.vacancy_id and vs.skills_id == s.id;