"""HuggingFace RAG Trainer"""

from typing import TYPE_CHECKING, Any, Callable, cast

from typing_extensions import assert_never

from fed_rag.base.trainer import BaseTrainer
from fed_rag.base.trainer_manager import BaseRAGTrainerManager, RAGTrainMode
from fed_rag.data_structures.results import TestResult, TrainResult
from fed_rag.decorators import federate
from fed_rag.exceptions import (
    MissingExtraError,
    UnspecifiedGeneratorTrainer,
    UnspecifiedRetrieverTrainer,
)

try:
    from datasets import Dataset

    _has_huggingface = True
except ModuleNotFoundError:
    _has_huggingface = False


if TYPE_CHECKING:  # pragma: no cover
    from datasets import Dataset
    from sentence_transformers import SentenceTransformer

    from fed_rag.fl_tasks.huggingface import HFModelType, HuggingFaceFLTask


class HuggingFaceRAGTrainerManager(BaseRAGTrainerManager):
    """HuggingFace RAG Trainer Manager"""

    def __init__(
        self,
        mode: RAGTrainMode,
        retriever_trainer: BaseTrainer | None = None,
        generator_trainer: BaseTrainer | None = None,
        **kwargs: Any,
    ):
        if not _has_huggingface:
            msg = (
                f"`{self.__class__.__name__}` requires `huggingface` extra to be installed. "
                "To fix please run `pip install fed-rag[huggingface]`."
            )
            raise MissingExtraError(msg)
        super().__init__(
            mode=mode,
            retriever_trainer=retriever_trainer,
            generator_trainer=generator_trainer,
            **kwargs,
        )

    def _prepare_generator_for_training(self, **kwargs: Any) -> None:
        self.generator_trainer.model.train()

        # freeze generator
        if self.retriever_trainer:
            self.retriever_trainer.model.eval()

    def _prepare_retriever_for_training(
        self, freeze_context_encoder: bool = True, **kwargs: Any
    ) -> None:
        self.retriever_trainer.model.train()

        # freeze generator
        if self.generator_trainer:
            self.generator_trainer.model.eval()

    def _train_retriever(self, **kwargs: Any) -> TrainResult:
        if self.retriever_trainer:
            self._prepare_retriever_for_training()
            return self.retriever_trainer.train(**kwargs)
        else:
            raise UnspecifiedRetrieverTrainer(
                "Attempted to perform retriever trainer with an unspecified trainer."
            )

    def _train_generator(self, **kwargs: Any) -> TrainResult:
        if self.generator_trainer:
            self._prepare_generator_for_training()
            return self.generator_trainer.train(**kwargs)
        else:
            raise UnspecifiedGeneratorTrainer(
                "Attempted to perform generator trainer with an unspecified trainer."
            )

    def train(self, **kwargs: Any) -> TrainResult:
        if self.mode == "retriever":
            return self._train_retriever(**kwargs)
        elif self.mode == "generator":
            return self._train_generator(**kwargs)
        else:
            assert_never(self.mode)  # pragma: no cover

    def _get_federated_trainer(self) -> tuple[Callable, "HFModelType"]:
        if self.mode == "retriever":
            if self.retriever_trainer is None:
                raise UnspecifiedRetrieverTrainer(
                    "Cannot federate an unspecified retriever trainer."
                )
            retriever_train_fn = self.retriever_trainer.train
            retriever_module = self.retriever_trainer.model
            retriever_module = cast("SentenceTransformer", retriever_module)

            # Create a standalone function for federation
            def train_wrapper(
                model: "HFModelType",
                train_dataset: "Dataset",
                val_dataset: "Dataset",
            ) -> TrainResult:
                _ = retriever_train_fn()
                return TrainResult(loss=0)

            return (
                federate.trainer.huggingface(train_wrapper),
                retriever_module,
            )

        elif self.mode == "generator":
            if self.generator_trainer is None:
                raise UnspecifiedGeneratorTrainer(
                    "Cannot federate an unspecified generator trainer."
                )
            generator_train_fn = self.generator_trainer.train
            generator_module = self.generator_trainer.model

            # Create a standalone function for federation
            def train_wrapper(
                model: "HFModelType",  # TODO: handle union types in inspector
                train_dataset: "Dataset",
                val_dataset: "Dataset",
            ) -> TrainResult:
                _ = generator_train_fn()
                # TODO get loss from out
                return TrainResult(loss=0)

            return (
                federate.trainer.huggingface(train_wrapper),
                generator_module,
            )
        else:
            assert_never(self.mode)  # pragma: no cover

    def get_federated_task(self) -> "HuggingFaceFLTask":
        from fed_rag.fl_tasks.huggingface import HuggingFaceFLTask

        federated_trainer, _module = self._get_federated_trainer()

        # TODO: add logic for getting evaluator/tester and then federate it as well
        # federated_tester = self.get_federated_tester(tester_decorator)
        # For now, using a simple placeholder test function
        def test_fn(
            model: "HFModelType", eval_dataset: "Dataset"
        ) -> TestResult:
            # Implement simple testing or return a placeholder
            return TestResult(loss=0.42, metrics={})  # pragma: no cover

        federated_tester = federate.tester.huggingface(test_fn)

        return HuggingFaceFLTask.from_trainer_and_tester(
            trainer=federated_trainer,
            tester=federated_tester,
        )
