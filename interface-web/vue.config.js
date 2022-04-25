module.exports = {
    "transpileDependencies": [
        "vuetify"
    ],
    pwa: {
        themeColor: "#2196f3",
        msTileColor: "#2196f3",
        appleMobileWebAppCache: "yes",
        manifestOptions: {
            name: "Color your mood",
            short_name: "ColorBiennale",
            display: "standalone",
            background_color: "#2196f3"
        },
        iconPaths: {
            favicon32: 'img/icons/favicon-32x32.png',
            favicon16: 'img/icons/favicon-16x16.png',
            appleTouchIcon: 'img/icons/apple-touch-icon.png',
            maskIcon: 'img/icons/safari-pinned-tab.svg',
        }
    }
}