# ECSE 484 HW 10: Project Proposal

Joseph Chen (jxc1598@case.edu)

Benson Jin (bxj155@case.edu)

## Problem Statement

Neural networks are computationally expensive to run. Not everyone can afford to rent expensive AWS GPU or Google Cloud TPU instances to run their freshly trained models in production to promise low latency. This especially holds true when you're trying to use your model to serve millions of users.

CPU instances are much, much cheaper to host and consequently, are more scalable.

The goal of this project is to test the effect of different techniques on model inference speed and performance on AWS CPU instances and calculate the most cost efficient approach.

## Experimental Design & Procedure

`BERT` is widely used in production because it's an all-around good model for natural language processing applications.

The techniques we wanted to explore are:

## Approach

If time allows, we will create an API that consumes POST requests with sentences to process. However, for this proof of concept, we strictly focus on the raw inference speed (images/second).
