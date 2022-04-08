# KueskiChallenge

## Index

<ol>
  <li>Architecture</li>
  <li>AWS Services
    <ol>
      <li>S3 Information</li>
      <li>CodeCommit</li>
      <li>CodeBuild</li>
      <li>CodePipeline</li>
      <li>SNS</li>
      <li>CloudWatch Event Rule or EventBringe</li>
      <li>Lambdas</li>
      <li>Sagemaker</li>
    </ol>
  </li>
  <li>Repository structure</li>
</ol>

---
## 1.1 Architecture

> **Description:** The architecture idea for this challenge, It's get a pipeline with the ProcessingJob and TrainningJob in the same StepFunctions Workflow. The workflow is started by a rule on EventBrigde every first day of month, calling a Lambda Functions that this one gets all the parameters to execute StepFunction.
Finally, The architecture has a monitoring group where all metrics from Sagemaker would be save and sends an email by SNS Topic
>
>![Build](Documentation/images/MLArchitecture.png)

---

## 2. AWS Services
## 2.1 S3 Information
>**Bucket name**: kueski-challenge-dev <br>
>**Repository Path:** s3://kueski-challenge-dev/sources/  <br>
>**Dataset Input for the Workflow:** s3://kueski-challenge-dev/landing/ <br>
>**Preprocessing Output:** s3://kueski-challenge-dev/preprocessing/ <br>
>**Models Output**: s3://kueski-challenge-dev/train_models/

---
## 2.2. CodeCommit 
> Repository Link: https://git-codecommit.us-east-1.amazonaws.com/v1/repos/kueski-challenge
>
>Branchs:
>- main (This is the branch that CodeCommit sees)
>- dev
>
>![Build](Documentation/images/codecommit_1.PNG)

---
## 2.3. CodeBuild 
>| Name  | Source provider |  Repository |
>|---|---|---|
>| kueski-challenge-training-build-image  |  	Amazon S3 |  	kueski-challenge-dev/kueski-challenge/images/kueski-challenge-training.zip | 
>|  kueski-challenge-processing-build-image | 	Amazon S3  |  	kueski-challenge-dev/kueski-challenge/images/kueski-challenge-processing.zip |  
>| kueski-challenge-inference-build-image  |  	Amazon S3 |  kueski-challenge-dev/kueski-challenge/images/kueski-challenge-inference.zip|  
>
>
>![Build](Documentation/images/codebuild_1.PNG)

---
## 2.4. CodePipeline
>Project name: KueskiS3Deploy <br>
>Stages:
>>- Source: Read for any change in AWS CodeCommit Repository <br>
>>- Approval: Manual approval for review before deploy. Send an email by SNS Topic <br>
>>- Deploy: Deploy CodeCommit Repository in a specific S3 bucket <br> 
>
>![Pipeline](Documentation/images/codepipeline_1.PNG)

## 2.5. SNS

>Topic: KueskiPipelineApproval <br>
>Description: Sends an email when CodePipeline runs <br>
>![SNS](Documentation/images/sns_1.PNG)

## 2.6. CloudWatch Event Rule or EventBringe

>Rule: startStepFunction <br>
>Description: It's for stepfunction execution and retrainning model (every month)   <br>
>![Bridge](Documentation/images/eventbridge_1.PNG)

## 2.7. Lambdas 

>**API: getFeatures** <br>
>_Code_: src\scripts\lambdas\kueski-challenge-GetFeatures.py <br>
>![Features](Documentation/images/getFeatures_1.PNG)
>
> **API: getPrediction** <br>
> _Code:_ src\scripts\lambdas\kueski-challenge-GetPredictions.py <br>
> ![Prediction](Documentation/images/getPrediction_1.PNG)
>
>**Lambda Step Function: runStepFunction** <br>
>_Description:_ Set and sends parameters before starts StepFunctions Workflow

## 2.8. Sagemaker

> **PreprocessingJob** <br>
> _Code:_ src\scripts\sagemaker\kueski-challenge-preprocessing.py <br>
> _Container:_ kueski-challenge-processing:latest <br>
> ![Preprocessing](Documentation/images/preprocessing_1.PNG)
>
> **TrainningJobs** <br>
> _Code:_ src\scripts\sagemaker\kueski-challenge-preprocessing.py <br>
> _Container:_ kueski-challenge-trainning:latest <br>
>
> **Inference** <br>
> _Code:_ src\scripts\lambdas\kueski-challenge-GetPredictions.py <br>
> _Container:_ kueski-challenge-inference:latest <br>
> - Endpoint: KueskiEndpointModel
> - Endpoint Config: KueskiEndpointConfig
> - Model: KueskiModel
> 
> ![Endpoint1](Documentation/images/endpoint_1.PNG)
> ![Endpoint2](Documentation/images/endpoint_2.PNG)
> ![Endpoint3](Documentation/images/endpoint_3.PNG)

---
## 3. Repository structure

<ul>
  <li>ChallengeInfo --> Information from Challenge</li>
  <li>Documentation --> Resources and files links with Documentation
    <ul>
      <li>images --> Here're save all images from this document</li>
    </ul>
  </li>
  <li>src --> From here is where all scripts are save
    <ul>
      <li>resources --> Like the jsons that I used for StepFunction creation</li>
      <li>scripts
        <ul> 
            <li>lambdas --> Here are save the APIs scripts</li>
            <li>sagemaker --> Scripts from PreprocessingJob and TrainningJob</li>
            <li>state-machine --> Last json with all Workflow configuration</li>
        </ul> 
    </ul>
  </li>
</ul>
