\LoadClass[12pt]{article}			
% LUDIS2022 ir LU FMOF Matemātikas nodaļas diplomdarbu stila fails, 2022. gada versija
% Autori: Edmunds Cers, Dacei Pētersone, Mārai Delesai-Vēliņa, Leonora Pahirko			
% Nepieciešamās packages			
	\usepackage{graphicx, amsmath, amssymb, amsthm, amsfonts}		
\usepackage{float}			
% Noformējums			
	\linespread{1.3} %equals 1.5 spacing		
	\newcommand{\@spacingsize}{1.5}		
	\usepackage[a4paper, left=3cm, right=2cm, top=2cm, bottom=2cm]{geometry}		
			
% Noformējums attēlu un tabulu anotācijām			
\usepackage{booktabs}			
\usepackage{caption}			
			
\captionsetup[figure]{labelfont=it,textfont={bf},			
	justification=raggedright,singlelinecheck=false}		
\captionsetup[table]{labelfont=it,textfont={bf},justification=raggedleft,singlelinecheck=false,			
	labelsep={newline}}		
			
% PDF specifiskas iespējas			
%\usepackage{hyperref} %Šai komandai jābūt pamatfailā, šeit nedrīkst būt! Punktus jauc!		
			
% XeLaTeX specifiskas paketes			
	\usepackage{fontspec}		
	\usepackage{xunicode}		
	\usepackage{xltxtra} %		
			
% Valodu atbalsts			
	\usepackage{polyglossia}		
	\setdefaultlanguage{latvian}		
	\setotherlanguages{english,russian}		
			
% Fonti -- var rakstīt sistēmas fontu nosaukumus			
	\setmainfont[Mapping=tex-text]{Times New Roman}		
	\newfontfamily\russianfont{Times New Roman}		
			
% Speciālās nodaļas (t.i., bez numerācijas)			
	\newcommand{\specnodala}[1]{\newpage\addcontentsline{toc}{section}{#1}\section*{#1}}		
			
%Komanda, kuru ievietojot izveido atstarpi pirmajam nodaļas/sekcijas paragrāfam
\newcommand{\firstparskip}{\tiny {\color{white} skip }  

\normalsize}

% Nodaļu un apksnodalu formats			
	\usepackage[explicit]{titlesec}		
			
	\titleformat{name=\section,numberless}		
	{\filcenter\large\bfseries}{}{-0.5em}{\MakeUppercase{#1}}		
			
	\titleformat{\section}		
	{\normalfont\large\bfseries}{\thesection.\quad}{-0.5em}{\MakeUppercase{#1}}		
			
	\titleformat{\subsection}		
	{\normalfont\normalsize\bfseries}{\thesubsection.\quad}{-0.5em}{#1}		
			
	\titleformat{\subsubsection}		
	{\normalfont\normalsize}{\thesubsubsection.\quad}{-0.5em}{#1}		
			
	\titleformat{\subsubsubsection}		
	{\normalfont\normalsize\bfseries}{\thesubsubsubsection.\quad}{-0.5em}{#1}		
			
% Toc - Satura raditajs			
%	\usepackage{tocloft}		
%	\setlength{\cftbeforesecskip}{6pt}		
			
% Literaturas saraksts			
			
\newcommand{\literatura}[1]{%			
	\newpage\thispagestyle{empty}		
	\renewcommand{\baselinestretch}{1}		
	\bibliographystyle{plain}		
	\renewcommand\refname{Izmantot\={a} literat\={u}ra un avoti}		
	\addcontentsline{toc}{section}{Izmantot\={a} literat\={u}ra un avoti}\bibliography{#1}		
	\renewcommand{\baselinestretch}{\@spacingsize}		
}			
			
% Vienādojumu numerācija			
\numberwithin{equation}{section}

\renewcommand{\theequation}{\thesection.\arabic{equation}}
%Numurs pirms definīcijas, teorēmas (nevis aiz)		
\swapnumbers			
% Theorem tipa nosaukumi			
\theoremstyle{definition}			
	\newtheorem{definicija}{Defin\={\i}cija}[section]		
	\newtheorem{piezimed}{Piez\={\i}me}[section]		
	\newtheorem{pienemums}{Pie\c{n}\={e}mums}[section]%		
	\newtheorem{piemers}{Piem\={e}rs}[section]%		
\theoremstyle{plain}			
	\newtheorem{teorema}{Teor\={e}ma}[section]%		
	\newtheorem{apgalvojums}{Apgalvojums}[section]%		
	\newtheorem{lemma}{Lemma}[section]%		
	\newtheorem{sekas}{Sekas}[section]%		
	\newtheorem{piezime}{Piez\={\i}me}[section]		
\renewcommand\proofname{Pier\={a}d\={\i}jums}			
\newenvironment{pieradijums}{\begin{proof}}{\end{proof}}			

			
%%% R koda noformējums			
%Krāsu kodi  			
			
\newcommand{\ctext}[3][RGB]{%			
  \begingroup			
  \definecolor{hlcolor}{#1}{#2}\sethlcolor{hlcolor}%			
  \hl{#3}%			
  \endgroup			
}			
			
%Koda noformējums			
\usepackage{soul}			
\usepackage[usenames,dvipsnames,table,xcdraw]{xcolor}  			
\usepackage{listings} % R kodu noformejums			
\lstset{			
   language=R, basicstyle=\footnotesize, commentstyle=\ttfamily\color{green},			
   numbers=left, numberstyle=\ttfamily\color{gray}\footnotesize, stepnumber=1,			
   numbersep=5pt, backgroundcolor=\color{white}, showspaces=false, showstringspaces=false,			
   showtabs=false, frame=single, tabsize=2, captionpos=b, breaklines=true,			
   breakatwhitespace=false, title=\lstname, keywordstyle=\color{RoyalBlue},			
   commentstyle=\color{Gray}, stringstyle=\color{ForestGreen} }			
			
    			
%%% Titlepage un  dokumentara lapa			
	\newcommand{\autors}[1]{\author{#1}}		
	\newcommand{\@nosaukumsLB}{0}		
	\newcommand{\nosaukums}[1]{%		
		\title{#1}	
		\if \@nosaukumsLB 0	
			\renewcommand{\@nosaukumsLB}{\MakeUppercase{\@title}}
		\fi	
	}		
	\newcommand{\NOSAUKUMS}[1]{\renewcommand{\@nosaukumsLB}{#1}}		
	\newcommand{\@gads}{}		
	\newcommand{\gads}[1]{\date{#1}}		
	%\newcommand{\gads}[1]{\renewcommand{\@gads}{#1}}		
	\newcommand{\universityname}{Latvijas Universit\={a}te}		
	\newcommand{\universityshort}{LU}		
	\newcommand{\@fakultate}{}		
	\newcommand{\@fakultateD}{}		
	\newcommand{\fakultate}[1]{%		
		\renewcommand{\@fakultate}{#1 fakult\={a}te}	
		\renewcommand{\@fakultateD}{#1 fakult\={a}t\={e}}}	
	\newcommand{\@katedra}{}		
	\newcommand{\katedra}[1]{\renewcommand{\@katedra}{#1}}		
	\newcommand{\@vieta}{}		
	\newcommand{\vieta}[1]{\renewcommand{\@vieta}{#1}}		
	\newcommand{\@darbaveids}{}		
	\newcommand{\@darbaveidsLB}{0}		
	\newcommand{\darbaveids}[1]{%		
		\renewcommand{\@darbaveids}{#1}	
		\if \@darbaveidsLB 0	
			\renewcommand{\@darbaveidsLB}{\MakeUppercase{\@darbaveids}}
		\fi	
	}		
	\newcommand{\DARBAVEIDS}[1]{\renewcommand{\@darbaveidsLB}{#1}}		
	\newcommand{\@studapl}{}		
	\newcommand{\studapl}[1]{\renewcommand{\@studapl}{#1}}		
	\newcommand{\@vaditajs}{}		
	\newcommand{\vaditajs}[1]{\renewcommand{\@vaditajs}{#1}}		
	\newcommand{\@recenzents}{}		
	\newcommand{\recenzents}[1]{\renewcommand{\@recenzents}{#1}}		
	\renewcommand{\maketitle}{%		
		\renewcommand{\baselinestretch}{1}	
	\begin{titlepage}%		
	\begin{center}%		
		{\large \MakeUppercase{\universityname} \par}%	
		{\large \MakeUppercase{\@fakultate}\par}%	
		{\large \MakeUppercase{\@katedra} \par}%	
		\vspace{60mm}	
		{\LARGE \textbf{\@nosaukumsLB} \par}%	
		\vspace{10mm}	
		{\large \MakeUppercase \@darbaveidsLB\ \par}% 	
	\end{center}\par		
	\vskip 7em%		
	\begin{flushright}		
			Autors: \@author \\
			Studenta apliecības nr.: \@studapl \\
			Darba vadītājs: {\@vaditajs}\\ 
    	\end{flushright}		
		\vskip 12em%	
		{\centering\large \MakeUppercase{\@vieta} \@date\par}	
	\end{titlepage}%		
	\global\let\and\relax		
	\renewcommand{\baselinestretch}{\@spacingsize}		
	}		
	\newcommand{\@doklapa}{%		
		\newpage\thispagestyle{empty}	
		\renewcommand{\baselinestretch}{1} 	
  			
		{\@darbaveids} darbs \ ``\@title'' izstr\={a}d\={a}ts	\universityshort\ \@fakultateD.\par
		\vskip 2em%	
		Ar savu parakstu apliecinu, ka p\={e}t\={\i}jums veikts patst\={a}v\={\i}gi, izmantoti tikai taj\={a} nor\={a}d\={\i}tie inform\={a}cijas avoti un iesniegt\={a} darba elektronisk\={a} kopija atbilst izdrukai.\par	
		\vskip 2em	
		Autors: \@author\par	
		\vskip 2em	
		\hspace{4em}\begin{tabular}{cc}%	
			\underline{\hspace{10em}}\vspace{-2mm} &
			\underline{\hspace{8em}} \\
			\tiny{(paraksts)} &
			\tiny{(datums)}
		\end{tabular}	
		\vskip 4em%	
		Rekomend\={e}ju darbu aizst\={a}v\={e}\v{s}anai:\par	
		Vad\={\i}t\={a}js: \@vaditajs\par	
		\vskip 2em	
		\hspace{4em}\begin{tabular}{cc}%	
			\underline{\hspace{10em}}\vspace{-2mm} &
			\underline{\hspace{8em}} \\
			\tiny{(paraksts)} &
			\tiny{(datums)}
		\end{tabular}	
		\vskip 4em%	
		Recenzents: \@recenzents \par	
		\vskip 4em	
		\hspace{4	em}\begin{tabular}{cc}%
			\underline{\hspace{10em}}\vspace{-2mm} &
			\underline{\hspace{8em}} \\
			\tiny{(paraksts)} &
			\tiny{(datums)}
		\end{tabular}	
			
		\vskip 2em%	
		\begin{tabular}{lc}	
		Darbs iesniegts Matem\={a}tikas noda\c{l}\={a} \@date. gada \underline{\hspace{2em}}. {j\={u}nij\={a}.} \\	
		\end{tabular}\par	
		\vskip 3em	
		\begin{tabular}{c}%	
			\underline{\hspace{25em}}\vspace{-2mm} \\
			\tiny{(Dekāna pilnvarotā persona: vecākā metodiķe Inita Šneidere)}
		\end{tabular}	
		\vskip 3em%	
		Darbs aizst\={a}v\={e}ts \MakeLowercase{\@darbaveids} gala parbaud\={i}juma komisijas s\={e}d\={e}\par	
		\vskip 1em%	
		\@date. gada \underline{\hspace{2em}}. {j\={u}nij\={a}}.	
	}   		
			
	\AtEndDocument{\@doklapa}		
			
% Salabo objektu tulkojumus papildus polyglossia latviskojumiem, tai skaitā pareizi novieto punktus numerācijā			
\usepackage{fixlatvian}			

			
