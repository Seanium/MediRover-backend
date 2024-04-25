# backend

## 启动说明

运行 `app/main.py` 文件，启动后端服务，运行于 `http://localhost:5000/`

## 在线 API 文档

启动后端服务后，访问 `http://localhost:5000/apidocs/`，查看 API 资源。

> [**Flasgger**](https://github.com/flasgger/flasgger) 是一个 Flask 扩展，它从 API 中注册的所有 Flask 视图生成一个 OpenAPI 规范。Flasgger 带有一个内置的 SwaggerUI，允许可视化和交互 API 资源。Flasgger 易于使用，并与 Flask 框架集成。
>
> Flasgger 的优点包括：
>
> 1. 从 Flask 视图自动生成 OpenAPI 规范，避免手动编写繁琐的文档。
> 2. 内置的 **[SwaggerUI](https://apifox.com/apiskills/introduction-to-swagger-ui-3/)** 界面可以可视化和交互 API 资源，方便调试和测试。
> 3. 可以使用 YAML、Python 字典或 Marshmallow Schemas 定义模式，并提供数据验证功能。
> 4. 支持简单的函数视图或使用 @swag_from 装饰器和 SwaggerView 等高级用法。
> 5. 与 Flask-RESTful 兼容，支持使用资源和 swag 规范。
> 6. 支持使用 Marshmallow APISpec 作为规范的基本模板，提供更多灵活性和扩展性。
