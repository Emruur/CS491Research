# Scenarios:

## Admin
- ### Add company

## Company Admin:
- ### Create Recruiter 
- ### Edit company info


## Recruiter
- ### Send Interview Request
- ### View Interview Analysis
- ### Add job
- ### Add job guide

## Candidate
- ### Attend Interview
- ### View Interviw Status


### Scenario Specification for JobTalk

#### Scenario 1: System Administrator Adds a Company
**Actors**: System Administrator  
**Entry Conditions**: A company applies to use JobTalk.  
**Flow of Events**:
1. The system administrator receives the company's application.
2. The administrator creates a new company profile in the system.
3. The administrator generates a company admin user for the new company.
4. The system sends the initial credentials to the company admin via email.
5. The company admin logs in and changes these credentials.

#### Scenario 2: Company Admin Creates Recruiter Accounts
**Actors**: Company Admin  
**Entry Conditions**: Company admin accesses the system.  
**Flow of Events**:
1. The company admin creates recruiter accounts.
2. The system sends account credentials to recruiters via email.

#### Scenario 3: Company Admin Edits Company Information
**Actors**: Company Admin  
**Entry Conditions**: Company admin needs to update company details.  
**Flow of Events**:
1. The company admin logs in to the system.
2. The admin updates and saves the company information.

#### Scenario 4: Company Admin Adds Job and Interview Guide
**Actors**: Company Admin  
**Entry Conditions**: A new job position is available.  
**Flow of Events**:
1. The company admin logs into the system.
2. The admin adds the job listing to the system.
3. The admin assigns an interview guide to the job.

#### Scenario 5: Recruiter Sends Interview Invitation
**Actors**: Recruiter  
**Entry Conditions**: Candidates are selected for the interview.  
**Flow of Events**:
1. The recruiter prepares an interview invitation in the system.
2. The system sends the invitation to selected candidates.

#### Scenario 6: Recruiter Reviews Interview Analysis
**Actors**: Recruiter  
**Entry Conditions**: An interview has been completed.  
**Flow of Events**:
1. The recruiter logs into the system.
2. The recruiter accesses the interview analysis report.

#### Scenario 7: Candidate Attends Interview
**Actors**: Candidate  
**Entry Conditions**: Candidate receives an interview invitation.  
**Flow of Events**:
1. The candidate receives an email with a link to the interview platform.
2. The candidate participates in the interview and answers questions.

#### Scenario 8: Candidate Views Interview Score
**Actors**: Candidate  
**Entry Conditions**: Candidate has completed the interview.  
**Flow of Events**:
1. The candidate logs into the system.
2. The candidate views their interview score or status update.

#### Scenario 9: System Analyzes Interview
**Actors**: System (Interview Bot)  
**Entry Conditions**: Candidate completes the interview.  
**Flow of Events**:
1. The system analyzes the interview for specific criteria.
2. An analysis report is generated for the recruiter.
3. A score or status update is made available to the candidate.
