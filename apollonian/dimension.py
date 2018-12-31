from heapq import heappush,heappop

def numcircles(maxk,k0,k1,k2,k3):
    pq=[]
    heappush(pq,(k0,k1,k2,k3))
    heappush(pq,(2*(k1+k2+k3)-k0,k1,k2,k3))
    while True:
        k0,k1,k2,k3=heappop(pq)
        if k0>maxk: return len(pq)
        heappush(pq,(2*(k0+k2+k3)-k1,k0,k2,k3))
        heappush(pq,(2*(k0+k1+k3)-k2,k1,k0,k3))
        heappush(pq,(2*(k0+k1+k2)-k3,k1,k2,k0))
