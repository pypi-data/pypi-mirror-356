# i18n file generator

Provided multiple i18n.properties files, this will generate three Java classes Constants, Messages and ValidationMessages to link to the strings.

## Usage

call generator.runGenerator(files: list, Ressource: str, targetPath: str, i18nPackagePath:str = null).

- files: List of i18n files to be considered (e.g. ['i18n.properties', 'i18n_de.properties'])
- resourcePath: path to the resource directory where the i18n files are stored (e.g. r'.\backend\domain\src\main\resources')
- targetPath: path to the target Directory where the Java classes should be created (e.g. r'.\backend\domain\src\main\java\org\derbanz\app\domain\i18n')
- i18nPackagePath: path to the I18N class handling the Translation. If left null, getter methods are not auto generated (e.g. 'org.derbanz.app.domain.base.I18N')

The Directory paths can be either absolute or relative, and they can be either raw or escaped (e.g. r'.\backend\domain\src\main\resources', r'D:\Development\app\backend\domain\src\main\resources', '.\\\\backend\\\\domain\\\\src\\\\main\\\\resources')

## Example

```
from Banz_i18n_codegenerator import generator

# with getter methods
generator.run(['i18n_de.properties', 'i18n_en.properties'], 'D:\\\\Development\\\\app\\\\backend\\\\domain\\\\src\\\\main\\\\resources', r'.\backend\domain\src\main\java\org\derbanz\app\domain\i18n', 'org.derbanz.app.domain.base.I18N')

# without getter methods
generator.run(['i18n_de.properties', 'i18n_en.properties'], 'D:\\\\Development\\\\app\\\\backend\\\\domain\\\\src\\\\main\\\\resources', r'.\backend\domain\src\main\java\org\derbanz\app\domain\i18n')
```