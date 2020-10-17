// ==UserScript==
// @name         AES decription
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Desencripta un mensaje cifrado mediante algoritmo AES
// @author       John Bidwell
// @match        https://htmlpreview.github.io/?https://github.com/JohnBidwellB/criptografia/blob/tarea3/Tarea3/index.html
// @require      https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.0.0/crypto-js.min.js
// @grant        none
// ==/UserScript==

(function () {
	"use strict";

	const cipheredText = document.getElementsByClassName("algorithm")[0].id;

	let ciphertext = CryptoJS.enc.Base64.parse(cipheredText);

	// split iv y ciphertext
	let iv = ciphertext.clone();
	iv.sigBytes = 16;
	iv.clamp();
	ciphertext.words.splice(0, 4); // delete 4 words = 16 bytes
	ciphertext.sigBytes -= 16;

	let htmlKey = document.getElementsByClassName("algorithmKey")[0].id;
	htmlKey = CryptoJS.enc.Utf8.parse(htmlKey);

	/** Por el lado del cliente, solo es posible modificar la llave, por lo que
	 * en caso de querer cambiarla se debe agregar la nueva llave de 16 caracteres
	 * en la variable customKey
	 */
	let customKey = null;
	if (customKey && customKey.length === 16) {
		customKey = CryptoJS.enc.Utf8.parse(customKey);
	} else {
		customKey = null;
	}

	// desencriptado
	let decrypted = CryptoJS.AES.decrypt(
		{ ciphertext: ciphertext },
		customKey || htmlKey,
		{
			iv: iv,
			mode: CryptoJS.mode.CFB,
		}
	);

	const decryptedText = decrypted.toString(CryptoJS.enc.Utf8);
	if (decryptedText) {
		document.getElementById("title").innerHTML = "El mensaje oculto es";
		document.getElementById("decodedText").innerHTML = decryptedText;
	}
})();
