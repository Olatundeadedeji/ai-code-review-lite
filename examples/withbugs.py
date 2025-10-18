import os, subprocess

def insecure(cmd):
    # BAD: shell=True, user-controlled input
    subprocess.call(cmd, shell=True)

def calc(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t):
    return a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p+q+r+s+t


def insecure_more(cmd):
    # BAD: shell=True triggers Bandit finding
    import subprocess
    subprocess.Popen(cmd, shell=True)
    return True
