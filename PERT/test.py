from PERT import GenerateData, runPERTfor, dystrybuantaODWR, dystrybuanta
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st


n_probs = [100,1000,10000,100000]

datatypes = [0, 1, 2]

n_instances = [5,9,10,20,50,70,100]

n_instance = 9
for n_prob in n_probs:
       isdone = False
       while isdone == False:
              try:
                     t,sig,data = GenerateData(n_prob,n_instance,prep_data_type = 0,use_m_data = True)
                     isdone = True
              except:
                     print("ind poza zasięgiem")

       kde = st.gaussian_kde(data)

       ax2 = plt.subplot()
       
       x = np.linspace(min(data),
                     max(data), n_prob)
       title = "Gęstości uzyskane dla parametrów: \n  n prób = "+str(n_prob)+", n wielkość = "+str(n_instance)+", dane od prowadzacego."
       ax2.plot(x, kde(x))
       ax2.plot(x, st.norm.pdf(x,loc = t,scale = sig),
              'r-')
       ax2.legend(["estymowana gęstość","zakładana gęstość"])
       print(title)
       plt.title(title)
       plt.xlabel("Czas [Dni]")
       plt.ylabel("Procent [%]")
       # plt.show()    
       filename = "g_"+str(n_prob)+"np_"+str(n_instance)+"ni_makdata.png"
       plt.savefig("./PERT/plots/"+filename, format="png", dpi=300)
       plt.close()




for n_prob in n_probs:
       for n_instance in n_instances:
              for datatype in datatypes:
                     isdone = False
                     while isdone == False:
                            try:
                                   t,sig,data = GenerateData(n_prob,n_instance,prep_data_type = datatype,use_m_data = False)
                                   isdone = True
                            except:
                                   print("ind poza zasięgiem")
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
                     title = "Gęstości uzyskane dla parametrów: \n  n prób = "+str(n_prob)+", n wielkość = "+str(n_instance)+", nr typu gen. danych = "+str(datatype)+"."
                     print(title)
                     ax2.plot(x, kde(x))
                     ax2.plot(x, st.norm.pdf(x,loc = t,scale = sig),
                            'r-')
                     # ax.set_xlim(min(min(data),min(res.cdf.quantiles)),max(max(data),max(res.cdf.quantiles)))
                     ax2.legend(["estymowana gęstość","zakładana gęstość"])
                     
                     plt.title(title)
                     plt.xlabel("Czas [Dni]")
                     plt.ylabel("Procent [%]")
                     # plt.show()    
                     filename = "g_"+str(n_prob)+"np_"+str(n_instance)+"ni_"+str(datatype)+"dt.png"
                     plt.savefig("./PERT/plots/"+filename, format="png", dpi=300)
                     plt.close()


