import sys
import boto
import ansible

print(sys.path)

print("boto is at: " + boto.__file__)
print("ansible is at: " + ansible.__file__)
