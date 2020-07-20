CREATE TABLE IF NOT EXISTS Works (
    id INTEGER PRIMARY KEY,
    title TEXT,
    author TEXT,
    UNIQUE(title, author)
);

CREATE TABLE IF NOT EXISTS Chapters (
    id INTEGER PRIMARY KEY,
    workid INTEGER NOT NULL,
    chaptertitle TEXT,
    chapterindex INTEGER,
    UNIQUE(workid, chaptertitle),
    UNIQUE(workid, chapterindex),
    FOREIGN KEY(workid) REFERENCES Works(id)
);

CREATE TABLE IF NOT EXISTS Pages (
    id INTEGER PRIMARY KEY,
    chapterid INTEGER NOT NULL,
    rawdata BLOB,
    extension TEXT,
    pageindex INTEGER,
    UNIQUE(chapterid, pageindex),
    FOREIGN KEY(chapterid) REFERENCES Chapters(id)
);

CREATE VIEW IF NOT EXISTS CatalogView AS
SELECT
    Works.title,
    Works.author,
    Chapters.chaptertitle,
    COUNT(Chapters.chapterindex) AS numberofpages,
    Chapters.chapterindex
FROM
    Works
    LEFT JOIN Chapters ON Works.id = Chapters.workid
    LEFT JOIN Pages ON Chapters.id = Pages.chapterid
GROUP BY Works.title, Works.author, Chapters.chaptertitle, Chapters.chapterindex
ORDER BY Works.title ASC, Works.author ASC, Chapters.chapterindex ASC
;

CREATE VIEW IF NOT EXISTS WorksView AS
SELECT
    Works.title,
    Works.author,
    Chapters.chaptertitle,
    Chapters.chapterindex,
    Pages.rawdata,
    Pages.extension,
    Pages.pageindex
FROM
    Works
    INNER JOIN Chapters ON Works.id = Chapters.workid
    INNER JOIN Pages ON Chapters.id = Pages.chapterid
;

CREATE TABLE IF NOT EXISTS MiscFiles (
    filename TEXT,
    rawdata BLOB,
    PRIMARY KEY(filename)
);