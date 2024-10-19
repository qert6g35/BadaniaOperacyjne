from PERT import GenerateData, runPERTfor, dystrybuantaODWR, dystrybuanta
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st

n_prob = 10000
t,sig,data = GenerateData(n_prob,20)

# print(t)
# print(sum(data)/len(data))

# t,sig = runPERTfor("pert_wzor")
# res = st.ecdf(data)

# # X = np.linspace(0,1,100)
# ax = plt.subplot()
# res.cdf.plot(ax)
# x = np.linspace(0,
#                 max(res.cdf.quantiles), n_prob)
# ax.plot(x, st.norm.cdf((x - t)/sig),
#        'r-', alpha=0.6, label='norm pdf')
# ax.set_xlim(min(min(data),min(res.cdf.quantiles)),max(max(data),max(res.cdf.quantiles)))
# ax.legend(["empiryczna dystrybuanta","dystrybyuanta"])
# plt.show()

# print(t)
# print(sum(data)/len(data))

# t,sig = runPERTfor("pert_wzor")
kde = st.gaussian_kde(data)

# X = np.linspace(0,1,100)
ax2 = plt.subplot()
# res.plot(ax)

x = np.linspace(min(data),
                max(data), n_prob)

ax2.plot(x, kde(x))
ax2.plot(x, st.norm.pdf(x,loc = t,scale = sig),
       'r-', alpha=0.6, label='norm pdf')
# ax.set_xlim(min(min(data),min(res.cdf.quantiles)),max(max(data),max(res.cdf.quantiles)))
# ax.legend(["empiryczna dystrybuanta","dystrybyuanta"])
plt.show()


