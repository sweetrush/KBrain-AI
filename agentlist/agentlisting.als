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
@@ ################################################################################

1,Default        , Default Assistance     , Default.atx
1,General        , General Assisance      , General.atx

@@ Technical Agents - This help with Technical System 
@@ ################################################################################

2,Linux          , Linux Assistance       , linux_assistance.atx
2,Linux Cmd Expt , Linux CMD Assistance   , linux_cew.atx
2,Docker         , Docker Assistance      , Dockerassist.atx

@@ Programming Prompts 
@@ ################################################################################

2,Python         , Python Assistance      , Python_assistance.atx
2,Python Mobile  , PyMobile Assistance    , kivy.atx 
2,Prolog         , Prolog Assistance      , prolog.atx
2,Go             , Go Lang Assistance     , Go_Assistance.atx
2,React JS       , ReactJS                , ReactJS_assistance.atx
2,Bash           , Bash Assistance        , bashexpert.atx
2,SVnCL          , SVnCL Assistance       , sc_programmer.atx
2,WebDev          , WebDev Assistance     , webprogrammer.atx

@@ Cybersecurity Prompts 
@@ ################################################################################

2,RedTeam        , RedTeam Assistance     , Red_Team_Expert.atx
2,Nmap           , Nmap Assistance        , Nmap_expert.atx
2,Rust-Scan      , Rust Scan Assistance   , rustscan.atx

@@ Busniess Agents - These Help with Busniess Tasks 
@@ ################################################################################

3,ProposalDev    , Proposal Dev Assistant , proposaldev.atx
3,Report Writer  , Report Writer          , Report_Writer.atx
3,Preso Expert   , Preso Expert           , PresentationSlide.atx
@@ 3,2Ddotplan      , 2D Plot Assistance     , dotplanner.atx
3,Emailhelper    , EmailHelper Assistance , emailhelper.atx
3,BusniessExpert , BE Assistance          , BusniessExpert.atx

@@ Commented Agents 
@@ 3,BusniessLawyer , BL Assistance          , BN_Lawer.atx

@@ Agents that are for Testing
@@ ################################################################################

3,Youtube SMRY      , Youtube SMRY Assistant   , YSummaryExpert.atx
4,Subject Experts   , Subject Experts          , SubjectModeratorTeam.atx
4,SpecialAI         , Special Assistance       , specialai.atx

@@ Hugging Face Agents 
@@ ################################################################################

@@ Uncomment the following to allow them to be used
@@
@@ 4,hf_HacXGpt     , Hacker Gpt Advance Level, hf_HacXGpt.atx 
@@ 4,hf_CoderWriter , CodeWriter              , hf_codewriter.atx 