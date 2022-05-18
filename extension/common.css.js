const STYLES = `
    .krisp-root {
        all: initial;
        font-family: system-ui, sans-serif;
        font-size: 14px;

        --primary-bg: #fdfeff;
        --primary-text: #111111;
        --secondary-bg: #f3f4f6;
        --secondary-text: #9b9b9b;
        --hover-bg: #dde1e5;
        --active-bg: #cdcfd2;
        --translucent: rgba(249, 250, 251, .8);
        --transparent: rgba(249, 250, 251, 0);
        --search-highlight: #a6f1e1;

        position: fixed;
        top: 8px;
        right: 8px;
        width: calc(100vw - 16px);
        max-width: 400px;
        z-index: 2147483647;
        border-radius: 6px;
        color: var(--primary-text);
        background: var(--primary-bg);
        box-shadow: 0 2px 6px rgba(0, 0, 0, .16);
        border: 1px solid var(--active-bg);
        transition: height .4s;
    }

    header {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid var(--active-bg);
        padding: 4px 4px;
        box-shadow: 0 1px 4px rgba(0, 0, 0, .16);
    }

    header .logo {
        text-transform: uppercase;
        margin-left: 8px;
        color: var(--secondary-text);
    }

    header .logo strong {
        color: var(--primary-text);
    }

    header button.closeButton {
        cursor: pointer;
        border: 0;
        background: transparent;
        width: 1.5em;
        height: 1.5em;
        display: block;
        font-size: 18px;
        line-height: 1.5em;
        border-radius: 6px;
    }

    header button.closeButton:hover {
        background: var(--hover-bg);
    }

    details.summary {
        padding: 6px 12px;
        line-height: 1.4em;
        border-bottom: 1px solid var(--active-bg);
    }

    details.summary summary {
        cursor: pointer;
        padding: 2px 6px;
        border-radius: 4px;
        margin: -2px -6px;
    }

    details.summary summary:hover {
        background: var(--hover-bg);
    }

    ul.summaryText {
        padding-left: 18px;
        margin: 8px 0 0 0;
    }

    .summaryText li {
        margin-bottom: 8px;
    }

    .doc-list {
        max-height: calc(100vh - 64px);
        overflow-y: auto;
    }

    .doc-item {
        cursor: pointer;
        padding: 6px 12px;
        line-height: 1.4em;
        border-bottom: 1px solid var(--active-bg);
    }

    .doc-item:hover {
        background: var(--hover-bg);
    }

    .doc-title {
        font-weight: bold;
    }

    .doc-meta {
        font-size: 12px;
        color: #555;
    }

    a.doc-href {
        color: inherit;
        text-decoration: none;
    }

    a.doc-href:hover {
        text-decoration: underline;
    }

    /* loading animation */

    .loading-container {
        height: 72px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-sizing: border-box;
        padding: 0 32px;
    }

    .loading {
        width: 100%;
        flex-grow: 1;
        margin: 0;
        height: 3px;
        position: relative;
        background: var(--hover-bg);
        overflow: hidden;
    }

    @keyframes slider {
        0% {
            transform: translateX(-100%);
        }
        100% {
            transform: translateX(100%);
        }
    }

    .loading::after {
        content: '';
        display: block;
        height: 100%;
        width: 60%;
        padding-right: 40%;
        background-color: var(--primary-text);
        position: absolute;
        top: 0;
        left: 0;
        animation: slider 1s linear infinite;
    }
`;
