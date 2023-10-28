# Project TBD - Rules and Guidelines

## Platforms and Programs:
	- Language: Python
	- Codebase and annotations should be written in English
	- Programs: Visual Studio Code

## Dependencies: 
	- TBD

## Folder Structure:
	- The folders are structured as; RELEASE, TEST & DEV. 
	- The program is based in a folder with a version name. 
	- If the database file has additions or removals, a Data Migration has to be performed. An explanation and guide is to be found in the documentation folder. 
	- Below is an explanation of the three main states of the product:
		- RELEASE:
			- Here is the fully functional program after testing has concluded. Every version has its own folder and should never be edited. If a bug is found once released, a new test cycle has to be initiated and a new version number issued. 
			
		- TEST:
			- Once the new program is ready to be tested, it will be copied to this folder. Once this is done, the test can begin. Testing procedure can be found in the documentations folder. 
			- When testing has concluded, move the contents to the RELEASE folder and update the online application. 
		- DEV: 
			- The current dev environment. In this folder the program will be built and compiled. 
			

## Github
	- When working in the DEV folder, create your own branch before committing. 
	- Once a feature is ready for testing, contact an Admin to help with combine the code and folders. 
	- If in doubt, create a new branch and commit often!