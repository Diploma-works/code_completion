import {languages} from 'prismjs/components/prism-core'


class LanguageMeta {
    constructor(langId, prismLang, filename, context) {
        this.langId = langId;
        this.prismLang = prismLang;
        this.context = context;
        this.filename = filename;
        this.url = `https://${langId}.flcc.iml.aws.intellij.net/v1/complete/gpt`
    }

    static build(langId) {
        switch (langId) {
            case 'java':
                return new LanguageMeta(langId, languages.java, "HelloWorld.java", JAVA_SNIPPET)
            case 'python':
                return new LanguageMeta(langId, languages.python, "hello_world.py", PYTHON_SNIPPET)
            case 'kotlin':
                return new LanguageMeta(langId, languages.kotlin, "HelloWorld.kt", KOTLIN_SNIPPET)
        }
    }

    async complete(offset, api_key) {
        const request_body = {
            "started_ts": Date.now(),
            "filename": this.filename,
            "code": this.context,
            "offset": offset - 1,
            "prefix": "",
            "mode": "FULL_LINE",
            "num_iterations": 5,
            "beam_size": 6,
            "diversity_groups": 1,
            "diversity_strength": 0.3,
            "len_norm_base": 2.0,
            "len_norm_pow": 0.7,
            "top_n": 5,
            "only_full_lines": false,
            "group_answers": false,
            "context_len": -1,
            "min_prefix_dist": 0.2,
            "min_edit_dist": 0.0,
            "keep_kinds": ["short", "prob"]
        }
        return await fetch(this.url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8',
                'Authorization': api_key
            },
            body: JSON.stringify(request_body)
        })
    }
}

const JAVA_SNIPPET = `class HelloWorld {
    public static void main(String[] args) {
        S
`

const KOTLIN_SNIPPET = `fun main(args : Array<String>) {
    p
`

const PYTHON_SNIPPET = `if __name__ == "__main__":
    p
`

export default LanguageMeta;