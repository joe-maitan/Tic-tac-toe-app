const cookie = {
    set(name, value, days = 7, path='/') {
        const date = new Date();
        date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000); // Cookie expires after 7 days
        const expires = `; expires=${date.toUTCString()}`;
        document.cookie = `${name}=${encodeURIComponent(value)}${expires}; path=${path}`;
    },
    get(name) {
        const nameEQ = `${name}=`;
        const cookies = document.cookie.split(';');
        
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(nameEQ)) {
                const value = decodeURIComponent(cookie.substring(nameEQ.length));
                return value === "" ? null : value;
            }
        }
        return null;
    },
    delete(name, path = '/') {
        document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=${path}`;
    }
}

export default cookie;