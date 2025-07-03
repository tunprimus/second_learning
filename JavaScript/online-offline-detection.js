//@ts-check
'use strict';

/**
 * @description How to Check Internet Connection Status Using Async JavaScript
 * @author Dave Gray
 * @link https://gist.github.com/gitdagray/f310be81be217750fc9d2b233e2ae70c
 */

const checkOnlineStatus = () => {
  return new Promise(async (resolve) => {
    let resolved = false;
    // requests longer than 5s are considered "offline"
    const timer = setTimeout(() => {
      resolved = true;
      resolve(false);
    }, 5000);

    try {
      const online = await fetch("https://commons.wikimedia.org/wiki/File:1x1.png", {
				mode: "no-cors",
				cache: "no-cache",
			});
      clearTimeout(timer);
      if (!resolved) {
        resolve(online.status >= 200 && online.status < 300); // either true or false
      }
    } catch (err) {
      if (!resolved) {
        resolve(false); // definitely offline
      }
    }
  });
};


(function pollOnlineStatus() {
  setTimeout(async () => {
    const result = await checkOnlineStatus();
		console.log(result);
    const statusDisplay = document.getElementById("status");
    statusDisplay.textContent = result ? "Online" : "OFFline";
    pollOnlineStatus(); // self-calling timeout is better than setInterval for this
  }, 13000);
})()


window.addEventListener('load', async (evt) => {
	const statusDisplay = document.getElementById('status');
	statusDisplay.textContent = (await checkOnlineStatus()) ? 'Online' : 'Offline';
});
