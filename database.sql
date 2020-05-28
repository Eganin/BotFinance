CREATE TABLE budjet(
	codename VARCHAR(255) PRIMARY KEY ,
	budjet_limit_daily INT DEFAULT NULL 
);

CREATE TABLE category(
	codename VARCHAR(255) PRIMARY KEY ,
	name VARCHAR(255),
	is_base_expense BOOLEAN ,
	aliases TEXT DEFAULT NULL 
);

CREATE TABLE expenses(
	id INT PRIMARY KEY,
	amount INT ,
	date_create DATETIME , 
	category_name INT ,
	raw_text TEXT ,
	CONSTRAINT fk_expenses_category_name FOREIGN KEY(category_name)
	REFERENCES category(codename)
);

CREATE TABLE all_budjet(
	limit_mount INT 
);

INSERT INTO category(codename , name , is_base_expense , aliases)
VALUES 
	('products','продукты',true , 'еда'),
	('coffee','кофе', false,''),
	('dinner','обед',false ,'столовая , ланч , бизнес-ланч , бизнес ланч'),
	('cafe','кафе', false,'ресторан , кафе , кафешка'),
	('transport','обществ.транспорт', true,'метро , автобус , трамвай'),
	('taxi','такси',true,'яндекс такси , обычное такси'),
	('phone','телефон', true,'mtc , связь'),
	('books','книги', false,'книги , литература, книжки'),
	('internet','интернет', true,'интернет , услуги веб-провайдера'),
	('subscribe','подписки',false ,'подписка , подписки'),
	('game','игры',false,'игры , видео-игры , видеоигры'),
	('entertainment','развлечения', true, 'безделушки , поход в кино , поход в театр , выставка , прогулка'),
	('other' ,'остальное',true,'')