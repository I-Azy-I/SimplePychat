# SimplePyChat
SimplePyChat à été développé afin d'ajouter un travail pratique dans le travail de maturité fédérale suisse fait en binôme par JulienBerthod ainsi que moi-même sur le pair à pair.
## Concepte
SimplePyChat est  une messagerie instantanée programmée en python et fonctionnant en pair à pair. Pour rejoindre un groupe il faut ainsi connaitre au moins une personne du réseau. Les messages envoyés seront transmis à travers le réseau sans que tout le monde se connaissent.

## Feature
- Il est possible d'envoyer des fichiers en plus de message sur le réseau.
- Les noeuds partagent des voisins afin de ne pas les déconnecter du réseau s'ils partent
- Les messages font semblant d'être chiffré (ils le sont mais on n'avait aucune idée de ce que l'on faisait, je déduis qu'il est impossible que l'implémentation soit bonne)
- Avec certain antivirus, SimplePyChat pourrait causer des blue screen of the death sur windows :) (devrait être fix...)

## Usage
Cf README.txt fait à l'origine

## Conclusion
SimplePyChat est un petit logiciel de messagerie en pair à pair qui à le mérite de fonctionner. Il n'a aucune prétention en performances et scalabilité (même si sur le papier la taille du réseau n'a auncune limite) mais reste un super premier projet dont nous sommes fières et qui nous a appris les bases de la programmation.
