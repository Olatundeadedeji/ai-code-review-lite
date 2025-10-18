import os, subprocess

def insecure(cmd):
    # BAD: shell=True, user-controlled input
    subprocess.call(cmd, shell=True)

def calc(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t):
    return a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p+q+r+s+t
