import inspect
import json
import re
import xml.sax.saxutils
import logging
from enum import Enum
from typing import List, Optional, Any

"""

FONCTIONS SPÉCIFIQUES CHAIN


"""


def search_wsp_code(portal, title: Optional[str] = None, title_fragment: Optional[str] = None, alias: Optional[str] = None, is_drf: Optional[bool] = None,
                    drf_Ref_wsp: Optional[str] = None, is_drv: Optional[bool] = None, drv_axis: Optional[str] = None, drv_master: Optional[str] = None,
                    is_public: Optional[bool] = None, wsp_key: Optional[str] = None, wsp_uri: Optional[str] = None, wsp_version: Optional[str] = None,
                    wsp_lang: Optional[str] = None, portlet_code: str = "chain") -> Optional[str]:
	"""
	Recherche un wspCode à partir d'un certain nombre de critères. Le code retourné est celui du premier wsp qui respecte tous les critères.
	:param portal: l'objet ScPortal concerné
	:param title: recherche exacte par le titre de cet atelier
	:param title_fragment: recherche un wsp dont le titre contient title_fragment
	:param alias: recherche par l'alias de l'atelier
	:param is_drf: recherche un atelier calque de travail
	:param drf_Ref_wsp: recherche un atelier calque de travail par le code de l'atelier de référence
	:param is_drv: recherche un atelier dérivé
	:param drv_axis: recherche un atelier dérivé par le code de dérivation
	:param drv_master: recherche un atelier dérivé par le code de l'atelier maître
	:param is_public: recherche un atelier publique
	:param wsp_key: recherche un atelier par la clé du modèle documentaire (par exemple 'Opale')
	:param wsp_uri: recherche un atelier l'URI du modèle documentaire (par exemple 'Opale_fr-FR_5-0-3')
	:param wsp_version: recherche un atelier par la version du modèle documentaire (par exemple '5.0.3')
	:param wsp_lang: recherche un atelier par langue du modèle documentaire (par exemple 'fr-FR')
	:param portlet_code: le code du portlet sur lequel faire la recherche ("chain" par défaut, spécifier ce paramètre pour le changer)
	:return: le code du wsp trouvé. None si aucun wsp trouvé.
	"""
	for wsp in __p(portal, portlet_code).adminWsp.list()["wsps"]:
		if title is not None and wsp["title"] != title:
			continue
		if title_fragment is not None and title_fragment not in wsp["title"]:
			continue
		if alias is not None and hasattr(wsp, "alias") and wsp["alias"] != alias:
			continue
		if is_drf is not None and "drfMasterWsp" not in wsp["props"]:
			continue
		if drf_Ref_wsp is not None and ("drfRefWsp" not in wsp["props"] or wsp["props"]["drfRefWsp"] != drf_Ref_wsp):
			continue
		if is_drv is not None and "drvAxis" not in wsp["props"]:
			continue
		if drv_axis is not None and ("drvAxis" not in wsp["props"] or wsp["props"]["drvAxis"] != drv_axis):
			continue
		if drv_master is not None and ("drvMasterWsp" not in wsp["props"] or wsp["props"]["drvMasterWsp"] != drv_master):
			continue
		if is_public is not None:
			if "publicWsp" not in wsp["props"]:
				if is_public:
					continue
			elif wsp["props"]["publicWsp"] == "false" and is_public or wsp["props"]["publicWsp"] == "true" and not is_public:
				continue
		if wsp_key is not None and wsp["wsp"]["wspType"]["key"] != wsp_key:
			continue
		if wsp_uri is not None and wsp["wsp"]["wspType"]["uri"] != wsp_uri:
			continue
		if wsp_version is not None and wsp["wsp"]["wspType"]["version"] != wsp_version:
			continue
		if wsp_lang is not None and wsp["wsp"]["wspType"]["lang"] != wsp_version:
			continue
		return wsp["wspCd"]
	return None


def create_or_update_wsp(portal, wsp_type_key: str, wsp_type_version: Optional[str] = None, wsp_type_lang: Optional[str] = None, wsp_type_options: Optional[list[any]] = None,  # wsp type
                         title: Optional[str] = None, alias: Optional[str] = None, desc: Optional[str] = None,  # Optional generic attributes
                         code: Optional[str] = None, folder_content: Optional[str] = None, folder_gen: Optional[str] = None,  # FS backend
                         skins: Optional[list[str]] = None, public: Optional[bool] = None, support_air_item: Optional[bool] = None, support_ext_item: Optional[bool] = None,  # Db Backend
                         wsp_drf_ref: Optional[str] = None, drf_title: Optional[str] = None,  # draft wsp
                         wsp_drv_master: Optional[str] = None, drv_axis: Optional[str] = None, drv_axis_path: Optional[list[str]] = None,  # drv wsp
                         scwsp: Optional[bytes] = None, local_file_path: Optional[str] = None,  # Import scwsp
                         portlet_code: str = "chain") -> str:
	"""
	Crée ou met un atelier à jour.
	Exemple d'appels :
	```python
	# Création ou mise à jour d'un atelier avec la dernière version d'Opale installée sur le serveur et l'extension Tutoriel (ex-Émeraude).
	create_or_update_wsp(portal, "Opale", wsp_type_options=[{"wsp_type_key":"OpaleExtEmeraude"}], title="Mon atelier Opale", alias="opale")

	# Création ou mise à jour d'un atelier avec la dernière version d'Opale 5 installée sur le serveur sans extension.
	create_or_update_wsp(portal, "Opale", wsp_type_version="5", title="Mon atelier Opale", alias="opale")

	# Création d'un atelier brouillon.
	create_or_update_wsp(portal, "Opale", alias="testDrf", wsp_drf_ref="opale", drf_title="Mon atelier brouillon")

	# Création d'un atelier dérivé.
	create_or_update_wsp(portal, "Opale", alias="testDrv", wsp_drv_master="opale", drv_axis="fc")

	# Création d'un second atelier dérivé dont le chemin de dérivation passe par le premier avant d'aller sur le master.
	create_or_update_wsp(portal, "Opale", alias="testDrv2", wsp_drv_master="opale", drv_axis="alternance", drv_axis_path=["fc"])

	```
	:param portal: l'objet ScPortal concerné
	:param wsp_type_key: la clé du modèle documentaire visé. Par exemple "Opale".
	:param wsp_type_version: la version cible du modèle documentaire. La dernière version est prise si ce paramètre est absent. Ce paramètre accepte au choix une version majeure ("5"), majeur et medium ("5.0") ou complète ("5.0.5"). Si la version n'est pas complète, la dernière version correspondante (la dernière 5 ou la dernière 5.0) sera utilisée.
	:param wsp_type_lang: la langue du modèle documentaire (par exemple "fr-FR" ou "en-US"). Si non précisé, le premier modèle correspondant aux autres critères est sélectionné.
	:param wsp_type_options: les extensions à utiliser. Ce paramètre attend un tableau de dict {wsp_type_key:str, wsp_type_version:Option[str], wsp_type_lang:Option[str]}
	:param title: le titre de l'atelier. Ce paramètre ne peut pas être utilisé lors de la création d'un atelier brouillon ou dérivé.
	:param alias: l'alias de cet atelier. L'alias se substitue au code de l'atelier. Il est unique et stable sur un même serveur. Fonction supportée uniquement en DB.
	:param desc: la description de l'atelier
	:param code: le code de cet atelier (FS uniquement). Le code est unique et stable sur un même serveur.
	:param folder_content: le chemin vers le dossier de l'atelier. Paramètre supporté uniquement pour la création d'un atelier sur un serveur FS.
	:param folder_gen: le chemin vers le répertoire des générations de cet atelier. Paramètre supporté uniquement pour la création d'un atelier sur un serveur FS.
	:param skins: les skins à utiliser avec cet atelier. Fonction supportée uniquement en DB.
	:param public: statut public de l'atelier. (pour être pointé par des items externes depuis d'autres ateliers). La fonction doit être permise dans la configuration du serveur. Fonction supportée uniquement en DB.
	:param support_air_item: activer la fonction des `air` items. La fonction doit être permise dans la configuration du serveur. Fonction supportée uniquement en DB.
	:param support_ext_item: activer la fonction des items externes. La fonction doit être permise dans la configuration du serveur. Fonction supportée uniquement en DB.
	:param wsp_drf_ref: ce paramètre permet de préciser que l'atelier créé est un atelier brouillon. Il doit contenir le wspCd ou l'alias vers l'atelier de référence. La fonction doit être permise dans la configuration du serveur. Fonction supportée uniquement en DB.
	:param drf_title: le titre de l'atelier brouillon.
	:param wsp_drv_master: ce paramètre permet de préciser que l'atelier créé est un atelier dérivé. Il doit contenir le wspCd ou l'alias vers l'atelier maître. La fonction doit être permise dans la configuration du serveur. Fonction supportée uniquement en DB.
	:param drv_axis: l'axe de dérivation d'un atelier dérivé.
	:param drv_axis_path: ce paramètre permet de définir le chemin de dérivation dans le cas où plusieurs ateliers sont dérivés d'un même atelier maître.
	:param scwsp: ce paramètre, valide uniquement pour une création d'atelier, permet d'importer un scwsp lors de la création de l'atelier (passé sous frome de bytes). Si ce paramètre est défini, les paramètres de wsp_type ne sont pas nécessaires. Si ce paramètre est défini, le paramètre local_file_path est ignoré.
	:param local_file_path: ce paramètre, valide uniquement pour une création d'atelier, permet d'importer un scwsp lors de la création de l'atelier (le paramètre contient le chemin vers le fichier scwsp). Si ce paramètre est défini, les paramètres de wsp_type ne sont pas nécessaires.
	:param portlet_code: le code du portlet sur lequel faire la recherche ("chain" par défaut, spécifier ce paramètre pour le changer).
	:return: le code de l'atelier créé.
	"""

	wsp_type_inst = None

	if hasattr(__p(portal, portlet_code), "adminOdb"):
		if code is not None:
			raise ValueError("code parameter is not supported on ODB chain backend")
		if folder_content is not None:
			raise ValueError("folder_content parameter is not supported on ODB chain backend")
		if folder_gen is not None:
			raise ValueError("folder_gen parameter is not supported on ODV chain backend")

	else:
		if skins is not None:
			raise ValueError("skins parameter is not supported on FS chain backend")
		if public is not None:
			raise ValueError("public parameter is not supported on FS chain backend")
		if support_air_item is not None:
			raise ValueError("support_air_item parameter is not supported on FS chain backend")
		if support_ext_item is not None:
			raise ValueError("support_ext_item parameter is not supported on FS chain backend")
		if wsp_drf_ref is not None:
			raise ValueError("wsp_drf_ref parameter is not supported on FS chain backend")
		if drf_title is not None:
			raise ValueError("drf_title parameter is not supported on FS chain backend")
		if wsp_drv_master is not None:
			raise ValueError("wsp_drv_master parameter is not supported on FS chain backend")
		if drv_axis is not None:
			raise ValueError("drv_axis parameter is not supported on FS chain backend")
		if drv_axis_path is not None:
			raise ValueError("drv_axis_path parameter is not supported on FS chain backend")

	if wsp_drf_ref is not None:
		if title is not None:
			raise ValueError("title can not be set on a draft wsp. Use drf_title to set the draft title")
		if wsp_drv_master is not None:
			raise ValueError("wsp_drv_master and wsp_drf_ref parameters can not be defined together")
		if drv_axis is not None:
			raise ValueError("drv_axis and wsp_drf_ref parameters can not be defined together")
		if drv_axis_path is not None:
			raise ValueError("drv_axis and wsp_drf_ref parameters can not be defined together")
		if scwsp is not None:
			raise ValueError("scwsp and wsp_drf_ref parameters can not be defined together")
		if local_file_path is not None:
			raise ValueError("local_file_path and wsp_drf_ref parameters can not be defined together")
		ref = __p(portal, portlet_code).adminWsp.info_wsp(wsp_drf_ref)
		if ref["status"] == "noWsp":
			raise ValueError(f"impossible to find a ref wsp with code or alias '{wsp_drf_ref}'")
		wsp_drf_ref = ref["wspCd"]

	elif wsp_drv_master is not None:
		if title is not None:
			raise ValueError("title can not be set on a drv wsp")
		if drf_title is not None:
			raise ValueError("drf_title and wsp_drv_master parameters can not be defined together")
		if scwsp is not None:
			raise ValueError("scwsp and wsp_drv_master parameters can not be defined together")
		if local_file_path is not None:
			raise ValueError("local_file_path and wsp_drv_master parameters can not be defined together")
		if drv_axis is None:
			raise ValueError("drv_axis axis is mandatory with parameter wsp_drv_master")

		master = __p(portal, portlet_code).adminWsp.info_wsp(wsp_drv_master)
		if master["status"] == "noWsp":
			raise ValueError(f"impossible to find a master wsp with code or alias '{wsp_drv_master}'")
		wsp_drv_master = master["wspCd"]

	if scwsp is not None:
		if wsp_type_key is not None:
			raise ValueError("wsp_type_key and scwsp parameters can not be defined together")
		if wsp_type_version is not None:
			raise ValueError("wsp_type_version and scwsp parameters can not be defined together")
		if wsp_type_lang is not None:
			raise ValueError("wsp_type_lang and scwsp parameters can not be defined together")
		if wsp_type_options is not None:
			raise ValueError("wsp_type_options and scwsp parameters can not be defined together")
		if code is not None:
			raise ValueError("code and scwsp parameters can not be defined together")

	elif local_file_path is not None:
		if wsp_type_key is not None:
			raise ValueError("wsp_type_key and local_file_path parameters can not be defined together")
		if wsp_type_version is not None:
			raise ValueError("wsp_type_version and local_file_path parameters can not be defined together")
		if wsp_type_lang is not None:
			raise ValueError("wsp_type_lang and local_file_path parameters can not be defined together")
		if wsp_type_options is not None:
			raise ValueError("wsp_type_options and local_file_path parameters can not be defined together")
		if code is not None:
			raise ValueError("code and local_file_path parameters can not be defined together")

	else:
		wsp_type_inst = __search_wsp_type_inst(portal, wsp_type_key, wsp_type_version, wsp_type_lang, wsp_type_options, portlet_code)
		if wsp_type_inst is None:
			raise ValueError(
				"unable to find wsp type. Check the paramaters wsp_type_key, wsp_type_version, wsp_type_lang and wsp_type_options or the installed wsppacks on the server")
	props = {"title": title, "desc": desc,
	         "code": code, "folderContent": folder_content, "folderGen": folder_gen,  # FS Props
	         "alias": alias, "skins": skins, "publicWsp": public, "airIt": support_air_item, "extIt": support_ext_item,  # DB Props
	         "wspRef": wsp_drf_ref, "draftTitle": drf_title, "wspMaster": wsp_drv_master, "drvAxis": drv_axis, "drvDefaultSrcFindPath": drv_axis_path
	         }
	props = {k: v for k, v in props.items() if v is not None}

	create = True
	wsp = None
	if alias is not None or code is not None:
		wsp = __p(portal, portlet_code).adminWsp.info_wsp(alias if code is None else code)
		create = wsp["status"] == "noWsp"
	if create:
		if scwsp is not None or local_file_path is not None:
			return __p(portal, portlet_code).adminWsp.create_wsp_import(params=props, data=scwsp if scwsp is not None else local_file_path)["wspCd"]
		else:
			return __p(portal, portlet_code).adminWsp.create_wsp(wsp_type=wsp_type_inst, params=props)["wspCd"]
	else:
		if "drfRefWsp" in wsp["props"]:
			if wsp_drf_ref is not None and wsp_drf_ref != wsp["props"]["drfRefWsp"]:
				raise ValueError(f"drfRefWsp is set to '{wsp['props']['drfRefWsp']}' and wsp_drf_ref is '{wsp_drf_ref}'. Changing drfRefWsp is forbidden")
			if wsp_drv_master is not None:
				raise ValueError("the wsp exists and has a drf status. Impossible to set wsp_drv_master parameter")
			if drv_axis is not None:
				raise ValueError("the wsp exists and has a drf status. Impossible to set drv_axis parameter")
			if drv_axis_path is not None:
				raise ValueError("the wsp exists and has a drf status. Impossible to set drv_axis_path parameter")
		elif "drvMasterWsp" in wsp["props"]:
			if wsp_drf_ref is not None:
				raise ValueError("the wsp exists and has a drv status. Impossible to set wsp_drf_ref parameter")
			if drf_title is not None:
				raise ValueError("the wsp exists and has a drv status. Impossible to set drf_title parameter")
		__p(portal, portlet_code).adminWsp.update_wsp_props(wsp_code=wsp["wspCd"], params=props)
		__p(portal, portlet_code).adminWsp.update_wsp_type(wsp_code=wsp["wspCd"], wsp_type=wsp_type_inst)
		return wsp["wspCd"]


"""

FONCTIONS SUR LE WSP


"""


def wsp_search(portal, wsp_code: str, request, portlet_code: str = "chain") -> List[List[Any]]:
	"""
	Appel au moteur de recherche d'un atelier.
	:param portal: l'objet ScPortal concerné
	:param wsp_code: le code de l'atelier ciblé
	:param request: la requête à envoyer au serveur
	:param portlet_code: le code du portlet sur lequel faire la recherche ("chain" par défaut, spécifier ce paramètre pour le changer)
	:return: une liste contenant une liste par résultat puis un champ par colonne définie dans la `request`.
	"""
	return __p(portal, portlet_code).search.search(wsp_code, request)["results"]


def wsp_get_item(portal, wsp_code: str, ref_uri: str, local_file_path: Optional[str] = None, portlet_code: str = "chain") -> Optional[str]:
	"""
	Récupération d'un item XML.
	:param portal: l'objet scPortal concerné
	:param wsp_code: le code de l'atelier concerné
	:param ref_uri: le chemin vers l'item (ou l'ID de l'item)
	:param local_file_path: si spécifié, l'item est téléchargé sur disque vers ce chemin
	:param portlet_code: le code du portlet sur lequel faire la recherche ("chain" par défaut, spécifier ce paramètre pour le changer)
	:return: Aucun retour si local_file_path est spécifié. Une str contenant l'item sinon.
	"""
	item = __p(portal, portlet_code).wspSrc.get_src(wsp_code, ref_uri)
	if local_file_path is not None:
		with open(local_file_path, "w") as file:
			file.write(item)
			return
	else:
		return item


def wsp_get_res(portal, wsp_code: str, src_uri: str, local_file_path: Optional[str] = None, portlet_code: str = "chain") -> Optional[bytes]:
	"""
	Récupération d'une ressource binaire.
	:param portal: l'objet scPortal concerné
	:param wsp_code: le code de l'atelier concerné
	:param src_uri: le chemin vers la ressource
	:param local_file_path: si spécifié, l'item est téléchargé sur disque vers ce chemin
	:param portlet_code: le code du portlet sur lequel faire la recherche ("chain" par défaut, spécifier ce paramètre pour le changer)
	:return: Aucun retour si local_file_path est spécifié. Une str contenant l'item sinon.
	"""
	uri = f"{src_uri}/{src_uri.split('/')[-1]}"
	binary = __p(portal, portlet_code).wspSrc.get_src_bytes(wsp_code, uri)
	if local_file_path is not None:
		with open(local_file_path, "wb") as file:
			file.write(binary)
			return
	else:
		return binary


def wsp_get_res_meta(portal, wsp_code: str, src_uri: str, local_file_path: Optional[str] = None, portlet_code: str = "chain") -> Optional[str]:
	"""
	Récupération des métadonnées d'une ressource binaire.
	:param portal: l'objet scPortal concerné
	:param wsp_code: le code de l'atelier concerné
	:param src_uri: le chemin vers l'item
	:param local_file_path: si spécifié, l'item est téléchargé sur disque vers ce chemin
	:param portlet_code: le code du portlet sur lequel faire la recherche ("uri = f"{src_uri}/{src_uri.split('/')[-1]}"chain" par défaut, spécifier ce paramètre pour le changer)
	:return: Aucun retour si local_file_path est spécifié. Une str contenant l'item sinon.
	"""
	uri = f"{src_uri}/meta.xml"
	item = __p(portal, portlet_code).wspSrc.get_src(wsp_code, uri)
	if local_file_path is not None:
		with open(local_file_path, "w") as file:
			file.write(item)
			return
	else:
		return item


def wsp_set_item(portal, wsp_code: str, ref_uri: str, item: Optional[str | bytes] = None, local_file_path: Optional[str] = None, portlet_code: str = "chain") -> None:
	"""
	Upload d'un item sur le serveur depuis une chaîne de caractères ou un fichier.
	:param portal: l'objet scPortal concerné
	:param wsp_code: le code de l'atelier concerné
	:param ref_uri: le chemin vers l'item (ou l'ID de l'item)
	:param item: le contenu de l'item au format `str` ou `bytes`. Ne peut pas être spécifié en doublon avec le paramètre `local_file_path`
	:param local_file_path: le chemin local sur le disque où récupérer le fichier XML de l'item à envoyer.
	:param portlet_code: le code du portlet sur lequel faire la recherche ("chain" par défaut, spécifier ce paramètre pour le changer)
	"""
	if item is None and local_file_path is None or item is not None and local_file_path is not None:
		raise ValueError("Only one of the parameters item and local_path could be defined")
	if item is not None:
		content = item
	elif local_file_path is not None:
		with open(local_file_path, "rb") as file:
			content = file.read()
	__p(portal, portlet_code).wspSrc.put_src(wsp_code, ref_uri, content)


def wsp_set_res(portal, wsp_code: str, src_uri: str, res: Optional[bytes] = None, local_file_path: Optional[str] = None, portlet_code: str = "chain") -> None:
	"""
	Upload d'un item sur le serveur depuis une chaîne de caractères ou un fichier.
	:param portal: l'objet scPortal concerné
	:param wsp_code: le code de l'atelier concerné
	:param src_uri: le chemin vers l'item
	:param res: le contenu du fichier binaire sous forme de `bytes`. Ne peut pas être spécifié en doublon avec le paramètre `local_file_path`
	:param local_file_path: le chemin local sur le disque où récupérer le fichier binaire à envoyer
	:param portlet_code: le code du portlet sur lequel faire la recherche ("chain" par défaut, spécifier ce paramètre pour le changer)
	"""
	if res is None and local_file_path is None or res is not None and local_file_path is not None:
		raise ValueError("Only one of the parameters item and local_path could be defined")
	if res is not None:
		content = res
	elif local_file_path is not None:
		with open(local_file_path, "rb") as file:
			content = file.read()
	__p(portal, portlet_code).wspSrc.put_src(wsp_code, src_uri, content)


def wsp_set_res_meta(portal, wsp_code: str, src_uri: str, meta: Optional[str | bytes] = None, local_file_path: Optional[str] = None, portlet_code: str = "chain") -> None:
	"""
	Upload d'un item sur le serveur depuis une chaîne de caractères ou un fichier.
	:param portal: l'objet scPortal concerné
	:param wsp_code: le code de l'atelier concerné
	:param src_uri: le chemin vers le fichier des métadonnées
	:param meta: le contenu des métadonnées au format `str` ou `bytes`. Ne peut pas être spécifié en doublon avec le paramètre `local_file_path`
	:param local_file_path: le chemin local sur le disque où récupérer le fichier XML de métadonnées à envoyer
	:param portlet_code: le code du portlet sur lequel faire la recherche ("chain" par défaut, spécifier ce paramètre pour le changer)
	"""
	uri = f"{src_uri}/meta.xml"
	if meta is None and local_file_path is None or meta is not None and local_file_path is not None:
		raise ValueError("Only one of the parameters item and local_path could be defined.")
	if meta is not None:
		content = meta
	elif local_file_path is not None:
		with open(local_file_path, "rb") as file:
			content = file.read()
	__p(portal, portlet_code).wspSrc.put_src(wsp_code, uri, content)


def wsp_send_scar(portal, wsp_code: str, ref_uri: str, send_props: dict[str, any], portlet_code: str = "chain") -> None:
	"""
	Envoie d'un scar par requête HTTP par le serveur depuis un portlet chain.
	:param portal: l'objet scPortal concerné
	:param wsp_code: le code de l'atelier concerné
	:param ref_uri: le chemin vers l'item (ou l'ID de l'item)
	:param send_props: ce paramètre optionnel permet d'envoyer le résultat de génération par une requête HTTP envoyée par le serveur. Valeur attendue : [package-lib].api.item.JSendProps
	:param portlet_code: le code du portlet sur lequel faire la recherche ("chain" par défaut, spécifier ce paramètre pour le changer)
	"""
	status_code = __p(portal, portlet_code).export.send_to(wsp_code, [ref_uri], send_props)
	if status_code != 200 and status_code != 204:
		logging.warning(f"The content has been sent by the serveur. The response is {status_code} (should be checked).")


def wsp_generate(portal, wsp_code: str, ref_uri: str, code_gen_stack: str, props: Optional[dict[str, Any]] = None,
                 send_props: Optional[dict[str, any]] = None, local_file_path: Optional[str] = None, portlet_code: str = "chain") -> Optional[bytes]:
	"""
	Lance puis télécharge une génération.
	:param portal: l'objet scPortal concerné
	:param wsp_code: le code de l'atelier concerné
	:param ref_uri: le chemin vers l'item (ou l'ID de l'item)
	:param code_gen_stack: le code du générateur
	:param props: dict optionnel pour spécifier des propriétés de génération
	:param send_props: ce paramètre optionnel permet d'envoyer le résultat de génération par une requête HTTP envoyée par le serveur. Valeur attendue : [package-lib].api.item.JSendProps
	:param local_file_path: si spécifié, la génération est téléchargée sur disque vers ce chemin
	:param portlet_code: le code du portlet sur lequel faire la recherche ("chain" par défaut, spécifier ce paramètre pour le changer)
	:return: Aucun retour si local_file_path ou send_props sont spécifiés. Des bytes contenant la génération sinon.
	"""
	__p(portal, portlet_code).wspGen.generate(wsp_code, ref_uri, code_gen_stack, props)
	gen_infos = __p(portal, portlet_code).wspGen.wait_for_generation(wsp_code, ref_uri, code_gen_stack)
	gen_status = gen_infos["status"]

	if gen_status == "warning":
		logging.warning(f"Generator {code_gen_stack} on {ref_uri} ended in warning status.")
	elif gen_status in ["failed", "null"]:
		logging.error(f"Generator {code_gen_stack} on {ref_uri} ended in {gen_status} status. Unable to download.")
		return

	if send_props is not None:
		status_code = __p(portal, portlet_code).wspGen.send_gen_to(wsp_code, ref_uri, code_gen_stack, send_props)
		if status_code != 200 and status_code != 204:
			logging.warning(f"The content has been sent by the server. The response is {status_code} (should be checked).")
		return

	if "mimeDownload" not in gen_infos or gen_infos["mimeDownload"] == "":
		return

	if local_file_path is not None:
		with open(local_file_path, "wb") as file:
			file.write(__p(portal, portlet_code).wspGen.download(wsp_code, ref_uri, code_gen_stack))
			return

	if local_file_path is None and send_props is None:
		return __p(portal, portlet_code).wspGen.download(wsp_code, ref_uri, code_gen_stack)


def wsp_export_scwsp(portal, wsp_code: str, local_file_path: Optional[str] = None, portlet_code: str = "chain") -> Optional[bytes]:
	"""
	Export un scwsp d'un atelier.
	:param portal: l'objet scPortal concerné
	:param wsp_code: le code de l'atelier
	:param local_file_path: si spécifié, l'item est téléchargé sur disque vers ce chemin
	:param portlet_code: le code du portlet sur lequel faire la recherche ("chain" par défaut, spécifier ce paramètre pour le changer)
	:return: Aucun retour si local_file_path est spécifié. Le scwsp sous forme de bytes sinon.
	"""
	b = __p(portal, portlet_code).export.export(wsp_code, [""])
	if local_file_path is not None:
		with open(local_file_path, "wb") as file:
			file.write(b)
			return

	return b


def wsp_export_scar(portal, wsp_code: str, ref_uri: str | list[str], include_items_graph: bool = True, keep_spaces: bool = False, local_file_path: Optional[str] = None,
                    portlet_code: str = "chain") -> Optional[bytes]:
	"""
	Export un scar depuis un ref_uri (espace ou item).
	:param portal: l'objet scPortal concerné
	:param wsp_code: le code de l'atelier
	:param ref_uri: le chemin vers l'item ou l'espace (ou son ID) racine de l'export (un tableau de chemins peut être passé dans ce paramètre)
	:param include_items_graph: inclure le réseau descendant complet de cet item
	:param keep_spaces: préserver les espaces de l'atelier
	:param local_file_path: si spécifié, l'item est téléchargé sur disque vers ce chemin
	:param portlet_code: le code du portlet sur lequel faire la recherche ("chain" par défaut, spécifier ce paramètre pour le changer)
	:return: Aucun retour si local_file_path est spécifié. Le scwsp sous forme de bytes sinon.
	"""
	b = __p(portal, portlet_code).export.export(wsp_code, ref_uris=[ref_uri] if ref_uri is str else ref_uri, scope="net" if include_items_graph else "node",
	                                            mode="wspTree" if keep_spaces else "rootAndRes")
	if local_file_path is not None:
		with open(local_file_path, "wb") as file:
			file.write(b)
			return
	return b


def wsp_import_scar(portal, wsp_code: str, scar: Optional[bytes] = None, local_file_path: Optional[str] = None, ref_uri: Optional[str] = None, replace_if_exist: bool = False,
                    portlet_code: str = "chain") -> None:
	"""
	Import d'un scar dans un atelier
	:param portal: l'objet scPortal concerné
	:param wsp_code: le code de l'atelier
	:param scar: le contenu du scar au format `bytes`. Ne peut pas être spécifié en doublon avec le paramètre `local_file_path`
	:param local_file_path: le chemin local sur le disque où récupérer le fichier scar à envoyer.
	:param ref_uri: le chemin vers le dossier vers lequel envoyer l'archive (par défaut, l'archive le contenu de l'archive est envoyé à la racine de l'atelier)
	:param replace_if_exist: Spécifier `True` pour permettre l'écrasement d'une ressource existante
	:param portlet_code: le code du portlet sur lequel faire la recherche ("chain" par défaut, spécifier ce paramètre pour le changer)
	"""
	__p(portal, portlet_code).importSvc.import_archive(wsp_code, content=scar if scar is not None else local_file_path, ref_uri_target=ref_uri, replace_if_exist=replace_if_exist)


"""

FONCTIONS SPÉCIFIQUES DÉPÔT


"""


def write_depot_request(portal, metas: dict[str, str], content: bytes | str = None, sync: bool = True, portlet_code: str = "depot") -> None:
	"""
	Envoi d'une requête en écriture sur le dépôt.
	:param portal: l'objet scPortal concerné
	:param metas: les métadonnées de la requête (ne pas indiquer les métadonnées "system" scContent ou createMetas
	:param content: si la requête inclut un contenu binaire, le contenu binaire ou le chemin vers le fichier
	:param sync: indiquer False pour basculer sur un envoi asynchrone. Une requête est envoyé à interval régulier jusqu'à fin du traitement.
	:param portlet_code: le code du portlet sur lequel faire la recherche ("depot" par défaut, spécifier ce paramètre pour le changer)
	"""
	if sync:
		resp = __p(portal, portlet_code).cid.sync_cid_request(metas=metas, content=content, return_props=["scCidSessStatus"])
	else:
		resp = __p(portal, portlet_code).cid.async_cid_request(metas=metas, content=content, return_props=["scCidSessStatus"])
	if resp["scCidSessStatus"] != "commited":
		raise RuntimeError(f"Cid request is not commited. Server returns {resp['scCidSessStatus']} status\nmetas sent: {json.dumps(metas)}")


"""

FONCTIONS GÉNÉRIQUES


"""


def list_users_or_groups(portal, include_users: bool = True, include_groups: bool = True, portlet_code: str = "chain") -> list[dict[str, any]]:
	"""
	Retourne la des utilisateurs et/ou groupes..
	:param portal: l'objet scPortal concerné
	:param include_users: si true, les accounts de type "user" seront inclus dans la liste retournée
	:param include_groups: si true, les accounts de type "group" seront inclus dans la liste retournée
	:param portlet_code: le code du portlet sur lequel faire la recherche ("chain" par défaut, spécifier ce paramètre pour le changer)
	:return: La liste des utilisateurs ou groupes. Chaque objet est un dict contenant les propriétés retournées par le serveur.
	"""
	options = {}
	if not include_users and not include_groups:
		return []

	if include_groups and not include_users:
		options["filterType"] = "group"

	if include_users and not include_groups:
		options["filterType"] = "user"
	return __p(portal, portlet_code).adminUsers.list(options)["userList"]


def create_or_update_user(portal, account: str, nick_names: Optional[list[str]] = None, first_name: Optional[str] = None, last_name: Optional[str] = None,
                          email: Optional[str] = None,
                          groups: Optional[list[str]] = None, roles: Optional[list[str]] = None, auth_method: Optional[str] = None, other_props: Optional[dict[str, any]] = None,
                          portlet_code: str = "chain") -> dict[str, any]:
	"""
	Crée ou met un utilisateur à jour.
	:param portal: l'objet scPortal concerné
	:param account: le compte de l'utilisateur
	:param nick_names: les surnoms (pseudos) de l'utilisateur (facultatif)
	:param first_name: le prénom de l'utilisateur (facultatif)
	:param last_name: le nom de famille de l'utilisateur (facultatif)
	:param email: l'email de l'utilisateur (facultatif)
	:param groups: les groupes de l'utilisateur (facultatif)
	:param roles: les rôles attribués à l'utilisateur (facultatif)
	:param auth_method: la méthode d'authentification de l'utilisateur (facultatif)
	:param other_props: objet contenant d'autres propriétés propres au backend de stockage des utilisateurs et la méthode d'authentification (password, pwdEndDt, etc.) (facultatif)
	:param portlet_code: Le code du portlet sur lequel faire la recherche ("chain" par défaut, spécifier ce paramètre pour le changer)
	:return: l'utilisateur sous forme d'un Dict.
	"""
	props = {"nickNames": nick_names, "firstName": first_name, "lastName": last_name, "email": email, "groups": groups, "grantedRoles": roles, "authMethod": auth_method,
	         "userType": "user", **(other_props if other_props is not None else {})}
	props = {k: v for k, v in props.items() if v is not None}
	if __p(portal, portlet_code).adminUsers.display(account) is not None:
		return __p(portal, portlet_code).adminUsers.update_user(account, props)
	else:
		return __p(portal, portlet_code).adminUsers.create_user(account, props)


def create_or_update_group(portal, account: str, group_name: Optional[str] = None, email: Optional[str] = None, groups: Optional[list[str]] = None,
                           roles: Optional[list[str]] = None,
                           portlet_code: str = "chain") -> dict[str, any]:
	"""
	Crée ou met un groupe à jour.
	:param portal: l'objet scPortal concerné
	:param account: le compte du groupe
	:param group_name: le nom du groupe (facultatif)
	:param email: l'email du groupe (facultatif)
	:param groups: les groupes auxquels appartient ce groupe (facultatif)
	:param roles: les roles attribués au groupe (facultatif)
	:param portlet_code: le code du portlet sur lequel faire la recherche ("chain" par défaut, spécifier ce paramètre pour le changer)
	:return: L'utilisateur sous forme d'un Dict.
	"""
	props = {"groupName": group_name, "email": email, "groups": groups, "grantedRoles": roles}
	props = {k: v for k, v in props.items() if v is not None}
	if __p(portal, portlet_code).adminUsers.display(account) is not None:
		return __p(portal, portlet_code).adminUsers.update_group(account, props)
	else:
		return __p(portal, portlet_code).adminUsers.create_group(account, props)


def set_granted_roles(portal, account: str, granted_roles: list[str], on_wsp_code: str = None, on_wsp_path: str = "", on_urltree_path: str = None,
                      auth_portlet_code="chain", chain_portlet_code: str = "chain", depot_portlet_code: str = "depot") -> None:
	"""
	Définit les rôles associés à un utilisateur au niveau du portal, d'un atelier, d'un espace de l'atelier ou d'un dossier du dépôt.
	Si on_wsp_code et on_urltree_path sont à None, les rôles sont modifiés au niveau du portal.
	Si on_wsp_code est défini et on_wsp_path est à None, les rôles sont modifiés au niveau de l'atelier.
	Si on_wsp_code et on_wsp_path sont définis, les rôles sont modifiés au niveau de l'espace de l'atelier.
	Si on_urltree_path est défini, les rôles sont modifiés au niveau du dossier du dépôt.
	:param portal: l'objet scPortal concerné
	:param account: le compte
	:param granted_roles: la liste des rôles associés à ce compte
	:param on_wsp_code: le code de l'atelier sur lequel définir les rôles
	:param on_wsp_path: l'espace de l'atelier sur lequel définir les rôles
	:param on_urltree_path: le path de l'URLtree sur lequel définir les rôles dans le dépôt
	:param auth_portlet_code: le code du portlet qui porte l'authentification (chain par défaut)
	:param chain_portlet_code: le code du portlet chain sur lequel définir les rôles d'un atelier ou espace (chain par défaut)
	:param depot_portlet_code: le code du portlet dépôt sur lequel définir les rôles d'un dossier de l'urlTree (depot par défaut)
	"""
	if on_wsp_code is None and on_urltree_path is None:
		__p(portal, auth_portlet_code).adminUsers.update_user(account, {"grantedRoles": granted_roles})

	if on_wsp_code is not None:
		__p(portal, chain_portlet_code).wspSrc.set_specified_roles(on_wsp_code, {account: {"allowedRoles": granted_roles}}, ref_uri=on_wsp_path)

	if on_urltree_path is not None:
		roles = __p(portal, depot_portlet_code).adminTree(on_urltree_path, "userRolesMap")
		roles[account] = {"allowedRoles": granted_roles}
		write_depot_request(portal, metas={"olderPath": on_urltree_path, "userRolesMap": roles}, portlet_code=depot_portlet_code)
	return


"""

FONCTIONS INTERNES


"""


def __search_wsp_type_inst(portal, wsp_type_key: str, wsp_type_version: Optional[str] = None, wsp_type_lang: Optional[str] = None, wsp_type_options: Optional[list[any]] = None,
                           portlet_code: str = "chain") -> Optional[any]:
	editor = __p(portal, portlet_code).wspMetaEditor.get_new_editor()
	candidate = None
	for wsp_type in editor:
		wsp_type.attrib["parsed-version"] = list(map(int, wsp_type.attrib["version"].split(".")))
		if wsp_type_key != wsp_type.attrib["key"]:
			continue
		if wsp_type_version is not None and not wsp_type.attrib["version"].startswith(wsp_type_version):
			continue
		if wsp_type_lang is not None and wsp_type_lang != wsp_type.attrib["lang"]:
			continue

		if candidate is None:
			candidate = wsp_type
		else:
			for i in range(0, len(candidate.attrib["parsed-version"])):
				if wsp_type.attrib["parsed-version"][i] > candidate.attrib["parsed-version"][i]:
					candidate = wsp_type
					break
				elif wsp_type.attrib["parsed-version"][i] < candidate.attrib["parsed-version"][i]:
					break

	if candidate is None:
		logging.error(f"No wsp type found for params wsp_type_key: '{wsp_type_key}', wsp_type_version= '{wsp_type_version}' and wsp_type_lang= '{wsp_type_lang}'.")
		return None

	# Recherche des options
	options = []
	if wsp_type_options is not None:
		for wsp_type_option in wsp_type_options:
			candidate_opt = None
			for wsp_type in candidate:
				wsp_type.attrib["parsed-version"] = list(map(int, wsp_type.attrib["version"].split(".")))
				if wsp_type_option["wsp_type_key"] != wsp_type.attrib["key"]:
					continue
				if "wsp_type_version" in wsp_type_option and not wsp_type.attrib["version"].startswith(wsp_type_option["wsp_type_version"]):
					continue
				if "wsp_type_lang" in wsp_type_option and wsp_type_lang != wsp_type_option["wsp_type_lang"]:
					continue

				if candidate_opt is None:
					candidate_opt = wsp_type
				else:
					for i in enumerate(candidate_opt.attrib["parsed-version"]):
						if wsp_type.attrib["parsed-version"][i] > candidate_opt.attrib["parsed-version"][i]:
							candidate_opt = wsp_type
							break
			if candidate_opt is None:
				logging.error(f"No wsp type option found for wsp type uri '{candidate.attrib['uri']}' and option params '{wsp_type_option}'.")
			else:
				options.append(candidate_opt)

	# Construction du wsp_type_inst
	wsp_type_inst = {"wspType": candidate.attrib}
	if len(options) > 0:
		wsp_type_inst["wspOptions"] = []
	for option in options:
		wsp_type_inst["wspOptions"].append(option.attrib)
	return wsp_type_inst


def __p(portal, portlet_code: str):
	"""
	Extrait le portlet depuis un ScPortal et le portlet code. Envoie une exception si le portlet n'est pas trouvé.
	"""
	if portlet_code not in portal:
		raise ValueError(f"Portlet {portlet_code} not found in ScPortal. The Portlet_code attribute should be specified")
	return portal[portlet_code]


def __docstring2dokiel(module, output):
	# 1 print module File
	output.write(
		'<?xml version="1.0"?><sc:item xmlns:dk="kelis.fr:dokiel" xmlns:sc="http://www.utc.fr/ics/scenari/v3/core" xmlns:sp="http://www.utc.fr/ics/scenari/v3/primitive"><dk:section>')
	output.write(
		f'<dk:sectionM><sp:title><dk:richTitle><sc:para xml:space="preserve">Documentation : Module {module.__name__[4:]}</sc:para></dk:richTitle></sp:title></dk:sectionM>')

	__browse_module_docstring2dokiel(module, output)

	output.write('</dk:section></sc:item>')


def __browse_module_docstring2dokiel(module, output):
	# module is file. print module content
	for name, obj in inspect.getmembers(module):
		if (inspect.isfunction(obj) or inspect.isclass(obj)) and obj.__module__ == module.__name__:
			output.write('<sp:content><dk:content>')
			__print_module_docstring2dokiel(module, output)
			output.write('</dk:content></sp:content>')
			break

	# module is package. Browse submodules
	for name, obj in inspect.getmembers(module):
		if inspect.ismodule(obj) and hasattr(obj, '__package__') and obj.__package__ == module.__name__:
			output.write('<sp:subSection><dk:section>')
			output.write(f'<dk:sectionM><sp:title><dk:richTitle><sc:para xml:space="preserve">Module {obj.__name__[4:]}</sc:para></dk:richTitle></sp:title></dk:sectionM>')
			__browse_module_docstring2dokiel(obj, output)
			output.write('</dk:section></sp:subSection>')


def __print_module_docstring2dokiel(module, output):
	# On affiche d'abord les fonctions
	for name, obj in inspect.getmembers(module):
		if hasattr(obj, '__doc__') and obj.__doc__ is not None and inspect.isfunction(obj) and not name.startswith("_") and obj.__module__ == module.__name__:
			output.write('<sp:complement>')
			output.write(f'<dk:blocTi><sp:rTitle><dk:richTitle><sc:para xml:space="preserve">{name}</sc:para></dk:richTitle></sp:rTitle></dk:blocTi>')
			output.write('<dk:flowAll><sp:txt><dk:text>')

			lines = getattr(module, name).__doc__.split("\n")
			for line in lines:
				if ":param" not in line and ":return:" not in line:
					output.write(f'<sc:para xml:space="preserve">{xml.sax.saxutils.escape(line)}</sc:para>')
			output.write('<sc:para xml:space="preserve">Arguments :</sc:para><sc:itemizedList>')
			for line in lines:
				if ":param" in line:
					extract_param_part = re.search(':param (.+):(.+)', line)
					key = extract_param_part.group(1)
					doc = extract_param_part.group(2).strip()
					output.write(f'<sc:listItem><sc:para xml:space="preserve">{xml.sax.saxutils.escape(key)} <sc:inlineStyle role="term">')
					if key in obj.__annotations__:
						type_name = str(obj.__annotations__[key])
						if type_name.startswith("<"):
							type_name = obj.__annotations__[key].__name__
						if type_name.startswith("typing"):
							type_name = type_name[7:]
						output.write(xml.sax.saxutils.escape(f'<{type_name}>'))
					elif key == "portal":
						output.write(xml.sax.saxutils.escape(f'<[lib_executable].ScPortal>'))
					output.write(f'</sc:inlineStyle> : {xml.sax.saxutils.escape(doc)}</sc:para></sc:listItem>')
			output.write('</sc:itemizedList>')
			for line in lines:
				if ":return:" in line:
					output.write(f'<sc:para xml:space="preserve">Retour : {xml.sax.saxutils.escape(line[9:])}</sc:para>')
			output.write('</dk:text></sp:txt></dk:flowAll></sp:complement>')

	# Puis les classes
	for name, obj in inspect.getmembers(module):
		if hasattr(obj, '__doc__') and inspect.isclass(obj) and obj.__doc__ is not None and obj.__module__ == module.__name__ and obj.__doc__ != "An enumeration.":
			output.write('<sp:part><dk:part>')
			output.write(f'<dk:rTitle><sp:rTitle><dk:richTitle><sc:para xml:space="preserve">Classe : {name}</sc:para></dk:richTitle></sp:rTitle></dk:rTitle>')
			output.write('<sp:co><dk:content>')

			output.write('<sp:infobloc><dk:blocTi/><dk:flowAll><sp:txt><dk:text>')
			lines = getattr(module, name).__doc__.split("\n")
			has_params = False
			for line in lines:
				if ":param" not in line:
					output.write(f'<sc:para xml:space="preserve">{xml.sax.saxutils.escape(line)}</sc:para>')
				else:
					has_params = True
			if has_params:
				output.write('<sc:para xml:space="preserve">Paramètres acceptés par le constructeur :</sc:para><sc:itemizedList>')
				for line in lines:
					if ":param" in line:
						output.write(f'<sc:listItem><sc:para xml:space="preserve">{xml.sax.saxutils.escape(line[7:])}</sc:para></sc:listItem>')
				output.write('</sc:itemizedList>')

			if issubclass(obj, Enum):
				output.write(f'<sc:para xml:space="preserve">Valeurs possibles : </sc:para><sc:itemizedList>')
				for field in obj:
					att_doc = __get_field_doc(obj, field.name)
					if att_doc is None or att_doc == "":
						continue
					if field.name == field.value:
						output.write(f'<sc:listItem><sc:para xml:space="preserve">{xml.sax.saxutils.escape(field.name)}')
					else:
						output.write(f'<sc:listItem><sc:para xml:space="preserve">{xml.sax.saxutils.escape(field.name)} ("{xml.sax.saxutils.escape(str(field.value))}")')
					output.write(f" : {xml.sax.saxutils.escape(att_doc)}")
					output.write("</sc:para></sc:listItem>")

				output.write('</sc:itemizedList>')

			elif obj.__class__.__name__ == "_TypedDictMeta":
				output.write(f'<sc:para xml:space="preserve">Champs de la structure de données : </sc:para><sc:itemizedList>')
				for key in obj.__annotations__:
					type_name = str(obj.__annotations__[key])
					if type_name.startswith("<"):
						type_name = obj.__annotations__[key].__name__
					if type_name.startswith("typing"):
						type_name = type_name[7:]
					output.write(f'<sc:listItem><sc:para xml:space="preserve">{xml.sax.saxutils.escape(key)} <sc:inlineStyle role="term">')
					output.write(xml.sax.saxutils.escape(f'<{type_name}>'))
					output.write(f'</sc:inlineStyle>')
					att_doc = __get_field_doc(obj, key)
					if att_doc is not None and att_doc != "":
						output.write(f" : {xml.sax.saxutils.escape(att_doc)}")
					output.write("</sc:para></sc:listItem>")

				output.write('</sc:itemizedList>')

			output.write('</dk:text></sp:txt></dk:flowAll></sp:infobloc>')
			for fun_name, fun_obj in inspect.getmembers(obj):
				if hasattr(fun_obj, '__doc__') and fun_obj.__doc__ is not None and inspect.isfunction(fun_obj) and not fun_name.startswith(
						"_") and fun_obj.__module__ == module.__name__:
					output.write('<sp:complement>')
					output.write(f'<dk:blocTi><sp:rTitle><dk:richTitle><sc:para xml:space="preserve">{fun_name}</sc:para></dk:richTitle></sp:rTitle></dk:blocTi>')
					output.write('<dk:flowAll><sp:txt><dk:text>')

					lines = getattr(obj, fun_name).__doc__.split("\n")
					for line in lines:
						if ":param" not in line and ":return:" not in line:
							output.write(f'<sc:para xml:space="preserve">{xml.sax.saxutils.escape(line)}</sc:para>')
					output.write('<sc:para xml:space="preserve">Arguments :</sc:para><sc:itemizedList>')
					for line in lines:
						if ":param" in line:
							output.write(f'<sc:listItem><sc:para xml:space="preserve">{xml.sax.saxutils.escape(line[7:])}</sc:para></sc:listItem>')
					output.write('</sc:itemizedList>')
					for line in lines:
						if ":return:" in line:
							output.write(f'<sc:para xml:space="preserve">Retour : {xml.sax.saxutils.escape(line[9:])}</sc:para>')
					output.write('</dk:text></sp:txt></dk:flowAll></sp:complement>')

			output.write('</dk:content></sp:co></dk:part></sp:part>')

	return


def __get_field_doc(obj, field_name):
	for line in inspect.getsourcelines(obj)[0]:
		if line.lstrip().startswith(field_name) and "[NON API]" in line:
			return line[line.index("#") + 1:].lstrip()
	return None
