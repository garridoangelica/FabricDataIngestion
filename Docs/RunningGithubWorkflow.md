### Steps to run GitHub workflow
1. Create app registration 
2. Create Entra ID group and add new App to Group
3. Go to Fabric, enable Service Principals and add group 
4. Add SPN to subscription as reader
5. Add SPN secret credentials in Github as FABRICSPN
     {
          "clid": "xxxxx",
          "seret": "xxxxx",
          "subid": "xxxxx",
          "tenid": "xxxxx"
      }
6. Add variables:
    - FABRIC_KUSTO_DATABASE
    - FABRIC_KUSTO_URI


This markdown is in the works. More step by steps coming soon!