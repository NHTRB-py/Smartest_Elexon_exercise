# Python exercise

This exercise is to get an insight into the candidate's coding capabilities. We are not looking for an application to be perfect but to see the candidate's ability to produce production worthy code. We will be evaluating the following:

	- The code's quality. Show us your tricks but bear in mind that needs to be maintained.
	- Its reliability. Automatic tests are encouraged.
	- Its easiness to be maintained by the team. Docstrings and a use guide are suggested.
	- Analysis process and data manipulation proficiency. Show us some analysis you do. 

You are expected to spend about 2-4 hours on this assignment.

### Optional Python install for Windows:  
Python does not need to be installed like this. If you have Python already on your machine then ignore these steps. This is just additional guidance.

1)	https://www.anaconda.com/products/individual    hit download  and install to C:\ProgramData    that will give you Python and loads of packages like pandas 
2)	If you want to use Pycharm to edit your code then https://www.jetbrains.com/pycharm/download/#section=windows and download community edition


### Guidelines

	- Work on your solution using a preferred version control system. Commit frequently and share a link to the final repository with us.
	- Document your code (readme or generated docs).
	- We value code quality. Use consistent and clean style across the codebase.
	- Make sure that your code can be executed without error and tests can be run and pass.
	- Use publicly available libraries, but keep in mind that your solution should be easily maintainable.
	- If you do not have time to complete the exercise please document what else would you do. 


### Requirements
We need to create a daily report of the system imbalance cost and price for the previous day using BMRS data. For that we need to collect data from their restful API. 

1. Create an api caller for BMRS Imbalance Prices (B1770) and Aggregated Imbalance Volumes (B1780). 
	 API documentation https://www.elexon.co.uk/documents/training-guidance/bsc-guidance-notes/bmrs-api-and-data-push-user-guide-2/. To obtain a API key is very simple and is well documented in the before user guide
2. Clean the inputs and produce two half hourly time series
3. Generate a message that provides the total daily imbalance cost and the daily imbalance unit rate.
4. Report which Hour had the highest absolute imbalance volumes.
5. Extra analysis or plotting will be appreciated. 

