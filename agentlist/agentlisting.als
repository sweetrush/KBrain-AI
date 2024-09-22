@@ 
@@ About::
@@ - This is the agent list File or Agent Flat-DB
@@ - Note that you should follow the following layout carefully. 
@@ - Developed by: SweetRushCoder.
@@ 
@@ How to Define agent:
@@  - First Column is the emjitag 
@@  - Second Column is the Agent Name 
@@  - Third Column is the Agent Label
@@  - Fourth Column is the Agent Context File
@@  - All columns are seperated with ","
@@  All Agent Context Files have the extension .atx
@@

@@ General Agents - Help with General Task
@@ #################################################################################################################################
@@ ID , Agent Name, Agent Alias, Agent PE File, Agent IMage, Agent Discription
@@ #################################################################################################################################

1,Default        , Default Assistance       , Default.atx               , defaut.png , The Main Default Agent for most things
1,General        , General Assisance        , General.atx               , defaut.png , For Simplied Formating Prompt very general
1,SpellChecker   , Spelling and Grammer     , SpellCheck.atx            , defaut.png , For Spelling and grammer Checker

@@ Technical Agents - This help with Technical System 
@@ #################################################################################################################################

2,Linux          , Linux Assistance         , linux_assistance.atx      , defaut.png , For all things Linux 
2,Linux Cmd Expt , Linux CMD Assistance     , linux_cew.atx             , defaut.png , For Asking any Linux Command only 
2,Docker         , Docker Assistance        , Dockerassist.atx          , defaut.png , For Docker question and Activities 

@@ Programming Prompts 
@@ #################################################################################################################################

2,Python         , Python Assistance        , Python_assistance.atx     , defaut.png , For Assisting with Python Coding 
2,Python Mobile  , PyMobile Assistance      , kivy.atx                  , defaut.png , For Assisting with Python Mobile Developments  
2,Php Coder      , Php Code Assistance      , PhpAssistance.atx         , defaut.png , Your Php Code assistance for all things Php
2,Prolog coder   , Prolog Assistance        , prolog.atx                , defaut.png , Your Prolog Code Assistance for Prolog 
2,Go Coder       , Go Lang Assistance       , Go_Assistance.atx         , defaut.png , Your Go Code Assistance for all things Go
2,React JS       , ReactJS                  , ReactJS_assistance.atx    , defaut.png , For Working with ReactJS Coding 
2,Bash           , Bash Assistance          , bashexpert.atx            , defaut.png , For all your Bash Scripting Needs 
2,SVnCL          , SVnCL Assistance         , sc_programmer.atx         , defaut.png , For your Server Client Programming
2,firefoxdev     , firefox Dev Assistance   , firefoxplugindev.atx      , defaut.png , For developing Firefox Plugins
2,WebDev         , WebDev Assistance        , webprogrammer.atx         , defaut.png , For all your Web Development Coding Needs

@@ Cybersecurity Prompts 
@@ ################################################################################################################################

2,CS-Expert      , Cybersecurity Expert      , CSExpert.atx            , defaut.png , For Cybersecurity Expert and Cybersecurity
2,RedTeam        , RedTeam Assistance        , Red_Team_Expert.atx     , defaut.png , For Cybersecurity Red Teaming Support 
2,Nmap           , Nmap Assistance           , Nmap_expert.atx         , defaut.png , For All your Nmap Scanning Questions
2,Rust-Scan      , Rust Scan Assistance      , rustscan.atx            , defaut.png , For All your Rust-Scan Needs 

@@ Busniess Agents - These Help with Busniess Tasks 
@@ ################################################################################################################################

3,ProposalDev         , Proposal Dev Assistant    , proposaldev.atx       , defaut.png  , For all your Proposal Needs 
3,Report Writer       , Report Writer             , Report_Writer.atx     , defaut.png  , For all your Report Development Needs
3,Preso Expert        , Preso Expert              , PresentationSlide.atx , defaut.png  , For Developmeing Slides and Presentations
@@ 3,2Ddotplan        , 2D Plot Assistance        , dotplanner.atx        , defaut.png  , For Drawing 2D Drawings 
3,Emailhelper         , EmailHelper Assistance    , emailhelper.atx       , defaut.png  , For all your email support needs 
3,BusniessExpert      , BE Assistance             , BusniessExpert.atx    , defaut.png  , A Busniess Expert Assistance 

@@ Commented Agents 
@@ 3,BusniessLawyer   , BL Assistance          , BN_Lawer.atx             , defaut.png  , Your Busniess Lawyer support 

@@ Language Supported Agents 
1, Chinese Translator , Chinese Trans_Interpt     , ChineseInterpiter.atx , defaut.png , For Chinese Translation and Interpretation

@@ Agents that are for Testing
@@ ################################################################################################################################

3,Youtube SMRY        , Youtube SMRY Assistant   , YSummaryExpert.atx        , defaut.png , For Summarising Youtube Videos
3,Subject Experts     , Subject Experts          , SubjectModeratorTeam.atx  , defaut.png , For Subject Matter Experts 
3,Social Media Poster , Social Media Post        , SocialMediaPost.atx       , defaut.png , For Social Media Posting Needs 
4,SpecialAI           , Special Assistance       , specialai.atx             , defaut.png , A special AI assistance for Labing Ideas

@@ Hugging Face Agents 
@@ ################################################################################

@@ Uncomment the following to allow them to be used
@@
@@ 4,hf_HacXGpt       , Hacker Gpt Advance Level , hf_HacXGpt.atx           , defaut.png , A Hacker Assistance for all thing Hackish
4,hf_CoderWriter   , CodeWriter               , hf_codewriter.atx           , defaut.png , A CodeWriter Assistant for Coding