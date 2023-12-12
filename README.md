
## pySynphasor
pySynphasor is a Scapy based python module for analyzing IEEE C37.118 protocol. The module can dissect and assemble synchrophasor packet. Therefore, the module can be utilized for  multiple purposes, such as:
1. Analyze the security vulnerabilities of IEEE C37.118 protocol 
2. Designing different types of attack such as FDIA, FCIA, eavesdropping, fuzz testing on the IEEE C37.118 protocol. 
3. Developing custom PMU and PDC application is also possible for specific purposes. 

>This project is a part of research project [Scalable Cyber-Physical Testbed for Cybersecurity Evaluation of Synchrophasors in Power Systems](https://arxiv.org/abs/2207.12610)

The detailed documentation and example is found  in the project website  **[shuvangkardas.com/pySynphasor](https://shuvangkardas.com/pySynphasor/)**

The pypi link of the project: [https://pypi.org/project/pySynphasor](https://pypi.org/project/pySynphasor/)

## Quick Start Guide
Install pySynphasor Library using the following command
```python
pip install pySynphasor
```

Then start using the library by importing as follows: 
```python
from pySynphasor.synphasor import *
```


## How to cite the paper
1. S. C. Das, T. Vu, H. Ginn, and K. Schoder, "Implementation of IEEE C37. 118 Packet Manipulation Tool, pySynphasor for Power System Security Evaluation," in 2023 IEEE Electric Ship Technologies Symposium (ESTS), 2023, pp. 542-548.

2. S. C. Das and T. Vu, “Scalable Cyber-Physical Testbed for Cybersecurity Evaluation of Synchrophasors in Power Systems,” _arXiv preprint arXiv:2207.12610_, 2022.

## How to contribute
- Please check TODO.md to find out where you can help us.
- Fork this repo.
- Create new branch: git checkout -b fixing-stupid-bug
- Commit changes: git commit -m 'There you go! Fixed the  stupid bug.'
- Push changes to the branch: git push origin fixing-your-stupid-bug
- Submit pull request.

## Credits
- [Shuvangkar Das](https://www.linkedin.com/in/shuvangkar/) - Research Assistant
- [Dr. Tuyen Vu](https://scholar.google.com/citations?user=xdlXvLUAAAAJ&hl=en) - Project Supervisor
 
## License
MIT

